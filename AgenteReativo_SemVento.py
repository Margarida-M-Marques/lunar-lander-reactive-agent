import gymnasium as gym
import numpy as np
import pygame

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
RENDER_MODE = None #seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
    continuous=True, gravity=GRAVITY, 
    enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
    turbulence_power=TURBULENCE_POWER)


def check_successful_landing(observation):
    x = observation[0]
    vy = observation[3]
    theta = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    legs_touching = contact_left == 1 and contact_right == 1

    on_landing_pad = abs(x) <= 0.2

    stable_velocity = vy > -0.2
    stable_orientation = abs(theta) < np.deg2rad(20)
    stable = stable_velocity and stable_orientation
 
    if legs_touching and on_landing_pad and stable:
        print("✅ Aterragem bem sucedida!")
        return True

    print("⚠️ Aterragem falhada!")        
    return False
        
def simulate(steps=1000,seed=None, policy = None):    
    observ, _ = env.reset(seed=seed)
    for step in range(steps):
        action = policy(observ)

        observ, _, term, trunc, _ = env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observ)
    return step, success


#Perceptions
def get_perceptions(observation):
    x = observation[0]
    vx = observation[2]
    vy = observation[3]
    theta = observation[4]
    vtheta = observation[5]
    contact_left = observation[6]
    contact_right = observation[7]
    
    # Definição das Percepções
    
    are_both_legs_touching = contact_left == 1 and contact_right == 1
    
    is_falling_fast = vy < -0.35
    
    
    
    abs_lim_angle = 0.18 # modulo do angulo limite maximo de inclinacao
        
    is_theta_lower_than_lim_min = theta < -abs_lim_angle
    is_theta_higher_than_lim_max = theta > abs_lim_angle
    
    is_rotating_right = vtheta < 0
    is_rotating_left = vtheta > 0
    
    
    
    target_treshold = 0.075 # permite a nave continuar a deslocar-se até uma margem de distancia
    
    is_target_on_right = x < target_treshold
    is_target_on_left = x > -target_treshold
    
    is_going_right = vx > 0
    is_going_left = vx < 0
    
    
    is_vtheta_speed_low = abs(vtheta) < 0.2 # verifica se a velocidade angular é baixa
    
    return is_target_on_left, is_going_right, is_target_on_right, is_going_left, is_vtheta_speed_low, is_falling_fast, is_rotating_right, is_rotating_left, is_theta_lower_than_lim_min, is_theta_higher_than_lim_max, are_both_legs_touching


# Actions
DESLIGAR = np.array([0,0]) # esta ação desliga os motores
PRINCIPAL = np.array([0.5,0]) # esta ação liga o motor principal
ESQUERDA = np.array([0.5,-1]) # esta ação liga o motor direito e o principal, permitindo rodar para a esquerda
DIREITA = np.array([0.5,1]) # esta ação liga o motor esquerdo e o principal, permitindo rodar para a direita


def reactive_agent(observation):
    is_target_on_left, is_going_right, is_target_on_right, is_going_left, is_vtheta_speed_low, is_falling_fast, is_rotating_right, is_rotating_left, is_theta_lower_than_lim_min, is_theta_higher_than_lim_max, are_both_legs_touching = get_perceptions(observation)
    
    if are_both_legs_touching:
        return DESLIGAR
    
    # impedir que a nave exceda os angulos limites
    
    if is_rotating_right and is_theta_lower_than_lim_min:
        return ESQUERDA
    
    if is_rotating_left and is_theta_higher_than_lim_max:
        return DIREITA
    
    
    # ir em direção ao alvo
    
    # ir para a direita
    if is_target_on_right and is_going_left and is_vtheta_speed_low:
        return DIREITA
    
    # ir para a esquerda
    if is_target_on_left and is_going_right and is_vtheta_speed_low:
        return ESQUERDA

    # impusionar a nave para cima
    if is_falling_fast:
        return PRINCIPAL
    

    # desligar motores, para permitir queda
    if True:
        return DESLIGAR



def keyboard_agent(observation):
    action = [0,0] 
    keys = pygame.key.get_pressed()
    
    print('observação:',observation)

    if keys[pygame.K_UP]:  
        action =+ np.array([1,0])
    if keys[pygame.K_LEFT]:  
        action =+ np.array([0,-1])
    if keys[pygame.K_RIGHT]: 
        action =+ np.array([0,1])

    return action
    

success = 0.0
steps = 0.0
for i in range(EPISODES):
    st, su = simulate(steps=1000000, policy=reactive_agent)

    if su:
        steps += st
    success += su
    
    if su>0:
        print('Média de passos das aterragens bem sucedidas:', steps/success*100)
    print('Taxa de sucesso:', success/(i+1)*100)

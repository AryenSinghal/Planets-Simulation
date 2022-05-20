import pygame, math
from sys import exit

# pygame initialisation
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Plenet Simulator')
FPS = 60

# colours
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

# planet class
class Planet():
    AU = 1.496e+8 * 1000
    G = 6.67428e-11
    SCALE = 15 / AU    # 1 AU = 15 px
    TIMESTEP = 3600 * 24 * 7   # 1 week

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.vel_x = 0
        self.vel_y = 0

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []
    
    def draw(self, screen):
        x = self.x * self.SCALE + WIDTH//2
        y = self.y * self.SCALE + HEIGHT//2

        if len(self.orbit) > 2:
            del self.orbit[:-10000]
            updated_points = [(x * self.SCALE + WIDTH//2, y * self.SCALE + HEIGHT//2) for x, y in self.orbit]
            pygame.draw.lines(screen, self.color, False, updated_points, 2)

        pygame.draw.circle(screen, self.color, (x,y), self.radius)

    def attraction(self, other):
        dist_x = other.x - self.x
        dist_y = other.y - self.y
        distance = math.sqrt(dist_x**2 + dist_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = (self.G * self.mass * other.mass) / distance**2
        theta = math.atan2(dist_y, dist_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_pos(self, planets):
        ttl_fx = ttl_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            ttl_fx += fx
            ttl_fy += fy
        
        self.vel_x += (ttl_fx / self.mass) * self.TIMESTEP
        self.vel_y += (ttl_fy / self.mass) * self.TIMESTEP

        self.x += self.vel_x * self.TIMESTEP
        self.y += self.vel_y * self.TIMESTEP
        self.orbit.append((self.x, self.y))


# main
def main():
    clock = pygame.time.Clock()

    # initialise planets
    sun = Planet(0, 0, 30, YELLOW, 1.9891 * 10**30)
    sun.sun = True
    
    mercury = Planet(-0.387 * Planet.AU, 0, 16, DARK_GREY, 3.285 * 10**23)
    mercury.vel_y = 47.4 * 1000
    venus = Planet(-0.7 * Planet.AU, 0, 16, WHITE, 4.867 * 10**24)
    venus.vel_y = 35.02 * 1000
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.97219 * 10**24)
    earth.vel_y = 29.783 * 1000
    mars = Planet(-1.5 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.vel_y = 24.077 * 1000
    jupiter = Planet(-5.2 * Planet.AU, 0, 30, 'brown', 1.898 * 10**27)
    jupiter.vel_y = 13.06 * 1000
    saturn = Planet(-9.5 * Planet.AU, 0, 30, 'antiquewhite3', 5.683 * 10**26)
    saturn.vel_y = 9.68 * 1000
    uranus = Planet(-19.8 * Planet.AU, 0, 30, BLUE, 8.681 * 10**25)
    uranus.vel_y = 6.08 * 1000
    neptune = Planet(-30 * Planet.AU, 0, 30, 'blue', 1.024 * 10**26)
    neptune.vel_y = 5.43 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                # scale
                if event.key == pygame.K_UP:
                    Planet.SCALE += 5 / Planet.AU
                elif event.key == pygame.K_DOWN:
                    Planet.SCALE -= 5 / Planet.AU
                
                # timestep
                if event.key == pygame.K_RIGHT:
                    Planet.TIMESTEP += 3600 * 24
                elif event.key == pygame.K_LEFT:
                    Planet.TIMESTEP -= 3600 * 24
        
        screen.fill('black')

        for planet in planets:
            if not planet.sun: planet.update_pos(planets)
            planet.draw(screen)

        pygame.display.update()    
        clock.tick(FPS)

main()
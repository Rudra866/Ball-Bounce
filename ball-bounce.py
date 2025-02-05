import pygame
import math
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
clock = pygame.time.Clock()

# ---------------------------
# Ball physics parameters
# ---------------------------
ball_radius = 10
ball_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
ball_vel = pygame.Vector2(5, -2)  # initial velocity
gravity = pygame.Vector2(0, 0.5)    # gravitational acceleration per frame
air_friction = 0.99               # slight damping of ball speed

# Collision parameters (when ball hits a wall)
restitution = 0.9   # Coefficient of restitution (bounciness in the normal direction)
wall_friction = 0.9 # Factor to reduce the tangential component

# ---------------------------
# Hexagon parameters
# ---------------------------
hex_center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
hex_radius = 200
hex_angle = 0                     # starting rotation angle (radians)
hex_angular_velocity = 0.01       # rotation speed (radians per frame)

# ---------------------------
# Helper functions
# ---------------------------
def get_hexagon_vertices(center, radius, angle_offset):
    """
    Returns the list of vertices (as pygame.Vector2 objects) for a hexagon
    centered at 'center', with circumradius 'radius', rotated by 'angle_offset'.
    """
    vertices = []
    for i in range(6):
        angle = angle_offset + i * (2 * math.pi / 6)
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        vertices.append(pygame.Vector2(x, y))
    return vertices

def closest_point_on_segment(A, B, P):
    """
    Given a segment AB and a point P, return the closest point on AB to P.
    """
    AB = B - A
    t = (P - A).dot(AB) / AB.length_squared()
    t = max(0, min(1, t))
    return A + t * AB

def handle_collision(ball_pos, ball_vel, ball_radius, A, B):
    """
    Checks and handles the collision between the ball (a circle with center ball_pos
    and radius ball_radius) and the line segment from A to B.
    
    The function:
      - Finds the closest point Q on the segment to the ball.
      - If the ball overlaps the wall (distance < ball_radius), it computes a
        collision response. In that response the wall’s velocity (from the hexagon’s
        rotation) is subtracted to work in the wall’s rest frame, the ball’s normal 
        velocity is reversed (with a little energy loss), and friction is applied 
        tangentially.
    """
    Q = closest_point_on_segment(A, B, ball_pos)
    d = (ball_pos - Q).length()
    if d < ball_radius:
        # Calculate how deep the ball is inside the wall
        penetration = ball_radius - d
        
        # Compute collision normal (from wall toward ball)
        if d != 0:
            normal = (ball_pos - Q).normalize()
        else:
            # Rare degenerate case: pick a normal perpendicular to the wall segment
            normal = pygame.Vector2(-(B - A).y, (B - A).x).normalize()
        
        # Push the ball out of the wall
        ball_pos += normal * penetration

        # Calculate the wall’s velocity at the collision point Q.
        # For a rigid body rotation, the velocity is given by
        # v_wall = omega × (Q - hex_center)
        r = Q - hex_center
        # In 2D, the perpendicular of r is (-r.y, r.x)
        v_wall = pygame.Vector2(-r.y, r.x) * hex_angular_velocity

        # Compute the ball’s velocity relative to the moving wall
        v_rel = ball_vel - v_wall
        
        # Decompose relative velocity into normal and tangential components:
        vn = normal * v_rel.dot(normal)
        vt = v_rel - vn
        
        # Reflect the normal component and apply restitution (energy loss)
        vn = -restitution * vn
        # Apply friction to the tangential component
        vt = wall_friction * vt
        
        # The new ball velocity is the sum of the adjusted relative components plus the wall velocity.
        ball_vel = vn + vt + v_wall
        
    return ball_pos, ball_vel

# ---------------------------
# Main simulation loop
# ---------------------------
running = True
while running:
    # Use dt to keep our simulation roughly frame-rate independent.
    # (Here we normalize dt so that dt=1 is roughly one frame at 60 FPS.)
    dt = clock.tick(60) / 16.67
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update the ball physics ---
    ball_vel += gravity * dt
    ball_pos += ball_vel * dt
    ball_vel *= air_friction

    # --- Update the hexagon rotation ---
    hex_angle += hex_angular_velocity * dt
    vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)

    # --- Check for collisions with each edge of the hexagon ---
    for i in range(len(vertices)):
        A = vertices[i]
        B = vertices[(i + 1) % len(vertices)]
        ball_pos, ball_vel = handle_collision(ball_pos, ball_vel, ball_radius, A, B)

    # --- Draw the scene ---
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (200, 200, 200),
                        [(v.x, v.y) for v in vertices], 3)
    pygame.draw.circle(screen, (255, 0, 0),
                       (int(ball_pos.x), int(ball_pos.y)), ball_radius)
    pygame.display.flip()

pygame.quit()
sys.exit()


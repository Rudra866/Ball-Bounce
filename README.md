# Bouncing Ball in a Spinning Hexagon

This project is a Python simulation that demonstrates a ball bouncing inside a spinning hexagon. The ball is affected by gravity, air friction, and bounces off the rotating walls with a realistic collision response. The simulation is built using [Pygame](https://www.pygame.org/).

## Features

- **Realistic Physics:**  
  The ball experiences gravity and air friction, creating a natural motion as it bounces around.

- **Rotating Hexagon:**  
  The hexagon rotates continuously, and its moving walls interact with the ball in a physically plausible way.

- **Accurate Collision Response:**  
  The collision response accounts for the wall's motion, separating the ball's velocity into normal and tangential components, applying restitution and friction.

---

## Requirements

- **Python 3.7 or higher**
- **Pygame** (to be installed in a virtual environment)

---

## Setting Up the Virtual Environment (Recommended)

1. **Clone or download the project:**  
   If you're using git, clone the repository:
   ```
   git clone https://github.com/yourusername/bouncing-ball-hexagon.git
   cd bouncing-ball-hexagon
   ```
Create a virtual environment:
Run the following command to create a virtual environment named ball_bounce_env:
```
python3 -m venv ball_bounce_env
```
Activate the virtual environment:

On macOS/Linux:
```
source ball_bounce_env/bin/activate
```
On Windows:
```
ball_bounce_env\Scripts\activate
```
Install Pygame:
Inside the activated virtual environment, install Pygame using pip:

```
pip install pygame
```
Run the simulation:
Once Pygame is installed, run the Python script:

```
python bouncing_ball_hexagon.py
```
Deactivate the virtual environment (when done):
To deactivate the virtual environment, simply run:

```
deactivate
```
Verifying the Installation
To confirm that Pygame was installed correctly, you can run:
```
python -m pygame.examples.aliens
```
If a small game window opens, the installation was successful.

Code Overview
Hexagon Generation:
The function get_hexagon_vertices(center, radius, angle_offset) calculates the vertices for a hexagon given a center, a radius, and a rotation offset.

Collision Detection:
For each hexagon edge, the program determines the closest point on that segment to the ball. If the ball is within its radius from that segment, a collision is detected.

Collision Response:
The function handle_collision(ball_pos, ball_vel, ball_radius, A, B) calculates the collision response by:

Computing the penetration depth.
Adjusting the ball's position to avoid overlap.
Accounting for the hexagon's angular velocity to compute the moving wall's velocity.
Separating and adjusting the ball's velocity into normal and tangential components, applying restitution and friction.
Main Loop:
The simulation loop updates the ball's position and velocity (with gravity and air friction), rotates the hexagon, checks for collisions, and renders the updated scene using Pygame.

Customization
You can adjust several parameters in the code to tweak the simulation behavior:

Ball Physics: Modify gravity, air_friction, and ball_vel for different motion characteristics.
Collision Response: Change restitution and wall_friction to adjust the bounciness and energy loss on collision.
Hexagon Rotation: Alter hex_angular_velocity to speed up or slow down the rotation.

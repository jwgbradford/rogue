import turtle

bob = turtle.Turtle()
bob.speed(0)
bob.shape('turtle')

red = 0
green = 0
blue = 1

delta_red = 0.05
delta_blue = 0.05
delta_green = 0.05

shape_size = 1
shape_angle = 100

while True:
    bob.color(red, green, blue)
    bob.forward(shape_size)
    bob.left(shape_angle)
    shape_size += 1
    red += delta_red
    if red > 1 or red < 0:
        if red > 1:
            red = 1
        else:
            red = 0
            
    delta_red *= -1
    green += delta_green        
    
    if green > 1 or green < 0:
        if green > 1:
            green = 1
        else:
            green = 0
        delta_green *= -1
        blue += delta_blue
    
    if blue > 1 or blue < 0:
        if blue > 1:
            blue = 1
        else:
            blue = 0
        delta_blue *= -1
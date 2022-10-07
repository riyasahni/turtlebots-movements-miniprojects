# warmup_project
Behavior: 'Driving in a square' assignment

High-level description of problem and approach: We were tasked with programming
our turtlebots to travel in a square. I used the /cmd_vec ROS topic to control 
the turtlebot's angular and linear velocities, and used the 'rospy.sleep()' 
function to control how long the turtlebot traveled linearly or angularly (to turn).
I programmed the turtlebot to travel linearly for roughly 3 seconds, then to turn at
a certain speed for 3 seconds so that it rotates at approximately a 90 degree angle,
and then it repeats by traveling linearly again for roughly 3 seconds, so on and so
forth.

Code explanation: I created an object called MoveRobotSquare. Inside, I create a 
class that initialized this object's rospy node, the publisher, 'move' as a Twist
message, and a counter that starts at 1. Then, I create a function called 'run',
which uses the counter to toggle back and forth between going straight or turning.
If the counter is even, then the robot turns for 3 seconds and if the counter is odd,
then the robot travels straight along its x-axis for 3 seconds. Before the while loop
cycles back, the counter is incremented by 1 and the robot's movement is published.
The MoveRobotSquare object is called and run at the bottom of the script. 

Gif:

![6w1mzp](https://user-images.githubusercontent.com/55162345/194470938-0234af31-18d9-434f-9972-5daf04ad1dee.gif)


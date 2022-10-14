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

Behavior: 'Person follower' assignment

High-level description of problem and approach: We were tasked with programming our 
turtlebots to follow a person and stop facing the front of the person. I used the /cmd_vec
and /scan ROS topics to control the turtlebot's linear and angular velocities. I first
scanned 360 degrees from the robot to locate the nearest object to the robot and the angle
that it was at to the robot. I created "buckets" of angles, so that if the object nearest
to the robot was within a specific angle bucket (i.e. within 0-45 degrees), then the
linear and angular velocities for the robot would be adjusted accordingly, so the robot would
rotate and move in that direction. This way, the robot was able to follow the person even
when the person kept moving.

Code explanation: I created an object called FollowPerson. INside, I create a class
that initialized this object's rospy node, the publisher, and default twist mesages that
are set to zero initially. Inside the process_scan function, I calculate what the nearest
object is away from the robot (whose distance from the robot is a non-zero value) and
I save the distance and the angle that it falls in. If the robot is already within set
distance from the person, then I stop or rotate to orient the robot towards the person.
Otherwise, I created angle buckets: 135-225, 45-135, 225-315 - so that when the 'min_angle'
falls within these buckets, the robot either flips around, turns right, or turns left to
keep following the person. 

Gif:

Behavior: 'Wall follower' assignment

High-level description of problem and approach: We were tasked with programming our
turtlebots to first locate a wall, go to it, and follow alongside it, making turns and
such. I used the /cmd_vel and /scan ROS topics to control the turtlebot's linear and
angular velocities. First I define a narrow angle bucket for the front of my robot and
a larger angle bucket that checks the left side of my robot. Once I've reached the set
distance from the front of the wall, then I turn right so that the wall is on the left-hand 
side of my robot. Then I adjust the robot slightly left or slightly right to keep the robot's
left-hand side roughly perpendicular with the wall at all times. When I encounter a wall in
front of the robot again, I turn. This way, the robot can make non-90 degree turns as well,
since it is programmed to adjust until it is perpendicular to a surface on its side, and
not make hard-programmed 90-degree turns.

Code explanation: I created an object called FollowWall. Inside, I create a class that initializes
the rospy node, the publisher, and the test messages are initially set to zero. In process_scan,
I initialize variables to keep track of the closest objects in front of and to the left of the
robot, as well as their respective angles (initialize as zero). Then, I scan the robot's
surroundings to set these variables equal to their minimum non-zero values (if they exist). Then,
I have a series of cases to account for the robot's situation. First, the robot is too far from
the closes object in front of it, so it moves towards the wall. Next, when the robot is set
distance from the wall, the robot will turn left. I have cases also adjust the robot so it
maintains a relatively perpendicular relationship between its left hand side and the wall after
it turns, so it can travel parallely. If the robot's nearest angle to the wall is not within the
85-95 degree bucket range, then it will either nudge right or nudge left to adjust. Otherwise,
if the robot is relatively parallel to the wall, it will keep going straight. Otherwise, if the
robot is directly in front of the wall within set distance range, then it just needs to turn
right. This way, the robot is not making fixed 90-degree turns when it follows along the wall.

Gif:

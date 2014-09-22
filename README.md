Friendly the Robot
==================

> A conspicuous lack of candy permeates the air.

![](http://s3.amazonaws.com/challengepost/photos/production/software_photos/000/161/887/datas/xlarge.png?1411309512)
![](http://s3.amazonaws.com/challengepost/photos/production/software_photos/000/161/888/datas/xlarge.png?1411309513)

Friendly the Robot is a jovial little robot that loves nothing more than sharing the delightful sweetness of Smarties with the world.

Built with Arduino, OpenCV, servomotors, and a whole lot of glue, Friendly is a robot among robots, a turret among a sea of Roombas.

Friendly's target audience is very wide: everyone! Able to track a large variety of faces, Friendly loves giving the gift of candy to anyone he meets!

Friendly is most proud of his main interactive implement - his 30fps Candy-Ray candy shooter, a bolt action, rubber-band-based, sugar-dispensing wonder.

Friendly the Robot is a turret-type robot that uses face detection and image processing to recognize human targets in need of candy. After identification, the targets are administered candy via slingshot.

A webcam connected to a computer obtains image data, which is then processed using Python and OpenCV to detect faces. Our Python script then calculates range, trajectory, and firing information and sends commands over the USB serial connection to the Arduino, which then controls the three servos to move into place and fire the slingshot.

Files
-----

Although we didn't manage to 3D print all of the designed parts, the parts we designed can be found in `Design/design.blend`. We simply exported each object to STL and had them 3D printed separately. The prints should be scaled such that the base object is 20cm by 20cm in area when viewed from above.

The individual part STL files can also be found in the `Design` folder.

The remainder of the mechanical parts were created using hand tools and Dremel. The parts we couldn't get 3D printed were improvised using cardboard, stiff plastic sheeting, and a lot of hastily applied hot glue.

The firing mechanism in particular is double layered plastic with a hand-cut channel and a coat hanger fashioned into a firing brace. Masking tape can be seen throughout, holding everything in place.

As for the software, the Arduino program can be found under the `Turret` folder. Simply upload the program and it will output servo control signals on Digital 9, 10, and 11. This program is designed for the Arduino Nano.

The program accepts commands via serial connetion, which you can test out in the Ardiino serial monitor. Type `y 23` to move the yaw servo to 23 degrees, `p 46` to set the pitch to 46 degrees, and 'f' to fire. Each command is terminated by a newline.

There are multiple standalone Python scripts in the project root folder. `test.py` is a script that tests face tracking and target aquisition, and is independent of the Arduino stuff. `control.py` is a script that tests Arduino and servo control via the USB serial connection, and is independent of the webcam stuff.

The `main.py` script is a script, independent of the other two, that runs the entire turret in face tracking mode. By default it fires in manual mode and aims using face tracking from webcam data. Make sure to adjust the coefficients and variables at the top of the script to account for your hardware differences.

About
-----

Friendly was built over one crazy, intense weekend at Hack the North 2014, billed as the "largest hackathon in Canada". Our team also built [MemoryTrain](https://github.com/KeriWarr/MemoryTrain) - check it out! Even though we didn't win any API prizes, building both these things was super fun and extremely rewarding in themselves.

I (Anthony Zhang) might post build logs and instructions on my blog in the future.

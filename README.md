# CrawlerIPX
Control a RC car via Ethernet using host-client TCP/IP protocol.
Host is hold using a Windows machine.
Currently built for Python version 3+

Client is created using RaspberryPi platform.
Currently built to run on RaspberryPi B 3, Raspbian Stretch OS


![alt text](https://github.com/scorpionipx/IPX-Crawler/blob/develop/104430660_2767072036885795_6971467355197687324_n.jpg?raw=true)

# NOTICE!!!
There are some setting needed to be configured on first run:
1. To enable wi-fi on rpi:
<ul>
<li> sudo apt-get update </li>
<li> sudo apt-get upgrade </li>
<li> sudo apt-get dist-upgrade </li>
<li> sudo rpi-update </li>
<li> [reboot] </li>
<li> sudo branch=next rpi-update </li>
<li> [reboot] </li>
</ul>
2. To enable video streaming on rpi (tutorial from https://pimylifeup.com/raspberry-pi-webcam-server/)
<br><br>
<p>To begin, first update the Raspberry Pi so you&#8217;re running on the latest version.</p><pre><code>sudo apt-get update
sudo apt-get upgrade</code></pre><p>Depending on the version of Raspbian you&#8217;re using you will need to do a few different steps.</p><h3>Raspbian Jessie</h3><p><strong class="step_numbering">1.</strong> We start by removing libraries that may conflict with the newer packages. These may or may not already exist on your copy of Raspbian.</p><pre><code>sudo apt-get remove libavcodec-extra-56 libavformat56 libavresample2 libavutil54</code></pre><p><strong class="step_numbering">2.</strong> Download and install the following packages by inserting the following commands into the terminal.</p><pre><code>wget https://github.com/ccrisan/motioneye/wiki/precompiled/ffmpeg_3.1.1-1_armhf.deb
sudo dpkg -i ffmpeg_3.1.1-1_armhf.deb</code></pre><p><strong class="step_numbering">3.</strong> Now we need to install the following packages, we will need these as the motion software relies on them.</p><pre><code>sudo apt-get install curl libssl-dev libcurl4-openssl-dev libjpeg-dev libx264-142 libavcodec56 libavformat56 libmysqlclient18 libswscale3 libpq5</code></pre><p><strong class="step_numbering">4.</strong> With those packages installed we can now grab the latest version of the motion software and install it. To do this run the following commands.</p><pre><code>wget https://github.com/Motion-Project/motion/releases/download/release-4.0.1/pi_jessie_motion_4.0.1-1_armhf.deb
sudo dpkg -i pi_jessie_motion_4.0.1-1_armhf.deb</code></pre><h3>Raspbian Stretch</h3><p><strong class="step_numbering">1.</strong> First install the following packages. This command will work both on the full and lite version of Raspbian Stretch.</p><pre><code>sudo apt-get install libmariadbclient18 libpq5 libavcodec57  libavformat57 libavutil55 libswscale4</code></pre><p><strong class="step_numbering">2.</strong>Next download the motion deb file from the GitHub and install it using the dpkg command.</p><pre><code>sudo wget https://github.com/Motion-Project/motion/releases/download/release-4.0.1/pi_stretch_motion_4.0.1-1_armhf.deb
sudo dpkg -i pi_stretch_motion_4.0.1-1_armhf.deb</code></pre><p>That&#8217;s all you need to do before moving on to configuring Motion so that it will run on your Pi.</p><h3>Configuring Motion</h3><p><strong class="step_numbering">1.</strong> Now we need to make some edits to the configuration file (motion.conf)</p><pre><code>sudo nano /etc/motion/motion.conf</code></pre><p><strong class="step_numbering">2.</strong> Find the following lines and change them to the following.</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> daemon on</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> stream_localhost off</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> <strong>Note:</strong> Change the following two lines from on to off if you&#8217;re having issues with the stream freezing whenever motion occurs.</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> output_pictures off</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> ffmpeg_output_movies off</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> <strong>Optional (Don&#8217;t include the text in brackets)</strong></p><p><strong class="step_numbering step_indent_left">&#9632;</strong> stream_maxrate 100 <em>(This will allow for real-time streaming but requires more bandwidth &#038; resources)</em></p><p><strong class="step_numbering step_indent_left">&#9632;</strong> framerate 100 (<em>This will allow for 100 frames to be captured per second allowing for smoother video</em>)</p><p><strong class="step_numbering step_indent_left">&#9632;</strong> width 640 <em>(This changes the width of the image displayed)</em></p><p><strong class="step_numbering step_indent_left">&#9632;</strong> height 480 <em>(This changes the height of the image displayed)</em></p><p><strong class="step_numbering">3.</strong> Now we need to setup up the daemon, first we need to edit the motion file.</p><pre><code>sudo nano /etc/default/motion</code></pre><p><strong class="step_numbering">4.</strong> Find the following line and change it to the following:</p><pre><code>start_motion_daemon=yes</code></pre><p><strong class="step_numbering">5.</strong> Once you&#8217;re done simply save and exit by pressing <em>ctrl+x</em> then <em>y</em>.</p><p><strong class="step_numbering">6.</strong> Now make sure the camera is connected and run the following line:</p><pre><code>sudo service motion start</code></pre><p><strong class="step_numbering">7.</strong> If you need to stop the service, simply run the following command:</p><pre><code>sudo service motion stop</code></pre><p><strong class="step_numbering">8.</strong> Now you should be able to check out the Webcam Stream at the IP address of our Pi so in your browser go to the following address:</p><pre><code>192.168.1.103:8081</code></pre><p><strong class="step_numbering">9.</strong> If the webpage isn&#8217;t loading try restarting the service.</p><pre><code>sudo service motion restart</code></pre>

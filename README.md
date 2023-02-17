# Auto-Photo-Colourizer
Colourize black and white images fast and with ease, cross platform, batch mode.

![Alt Text](https://github.com/Steve-Shambles/Auto-Photo-Colourizer/blob/main/screenshot-main-v162.png)

Important Note: The 122MB file "colorization_release_v2.caffemodel" is too big to upload here, but you can download it from here:

https://code.naturkundemuseum.berlin/mediaspherefornature/colorize_iiif/blob/master/experimental/model/colorization_release_v2.caffemodel

I have checked it downloads okay (it's very fast) and tested that it works. Add this file to the APC main dir with the other APC files.

Requirements: pip3 install matplotlib, numpy, opencv-python, pillow.


I started this project back in 2021, I have revived it and made a few tweaks and I'm hoping to make more improvements over time.

![Alt Text](https://github.com/Steve-Shambles/Auto-Photo-Colourizer/blob/main/screenshot-menu-colorizing-v162.png)


I spent a lot of time learning how to make this icon menu, was very proud I got it right at the time ;-)
![Alt Text](https://github.com/Steve-Shambles/Auto-Photo-Colourizer/blob/main/screenshot-menu-v162.png)


The AI model seems to be heavily trained for outdoor type scenes, they work best I feel.
![Alt Text](https://github.com/Steve-Shambles/Auto-Photo-Colourizer/blob/main/screenshot-deer-colourized.png)


Written in Python 3, using Opencv and Tkinter.

The A.I colourization algorithm was developed by Richard Zhang, Phillip Isola and Alexei A. Efros of Berkley University, California. 
With thanks to those guys for sharing.

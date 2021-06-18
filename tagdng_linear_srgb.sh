#!/bin/sh

exiftool -DNGVersion="1.4.0.0" -DNGBackwardVersion="1.4.0.0" -ColorMatrix1="3.240969942 -1.537383178 -0.4986107603 -0.9692436447 1.875967492 0.04155506008 0.0556300797 -0.2039769589 1.056971514" \
         -IFD0:BlackLevel="0" -IFD0:WhiteLevel=65281 \
         -PhotometricInterpretation="Linear Raw" -CalibrationIlluminant1=D50 \
         -SamplesPerPixel=3  -AsShotNeutral="1 1 1" -UniqueCameraModel="Xphase Pro S" \
	 -BitsPerSample="16 16 16" $1

A few scripts for fiddling with the Xphase Pro camera family for those who already own one.  Specifically, right now, an implementation of
UnpackORI that is not Wintel dependent.

As of June 14, 2021 - the camera is still heavily dependent on a JPEG-only workflow.  JPEGs are at least not in sRGB
colorspace/transfer function, but luma range is (roughly) 24-226, leaving almost 50
code values out of 255 nearly unused.  (Under some circumstances, code values outside of 24-226 are used, but rarely.  Pure black
clips to 24 and pure white to 226...)

The camera does now have a raw DNG option, although white balance is prescaled and the values are multiplied by 64 after
white balance prescaling to fill an int16 with huge histogram gaps, making files 60% larger than not scaling anything and saving bitpacked
data with BitsPerSample = 10

If you are asking - where's the EXIF?  The ORI file stores metadata in an unknown fully proprietary arrangement, and as a result this metadata cannot
be extracted and written out as EXIF.  The files within the ORI are JFIF images, not EXIF images (yes, there IS a difference! -
most people don't realize that because an EXIF image is named .jpg and almost universally only stores JPEG data and thus is almost
indistinguishable from metadata-less JFIF other than the lack of metadata.)

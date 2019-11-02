A few scripts for fiddling with the Xphase "pro" camera for those who already own one.  Specifically, right now, an implementation of
UnpackORI that is not Wintel dependent.

Why is "pro" in quotes?  Read the script.  A professional camera does not save images in sRGB JPEG with no option to save raw sensor data.

As of November 2, 2019, the camera ONLY saves JPEGs within a proprietary "ORI" container and the supposed "RAW DNG" functionality released
on October 31 is creating (apparently very broken) DNGs after stitching that are not RAW by any definition of the word.  Linear DNG would have been
semi-acceptable if the input data to stitching were raw bayer data, but the new knowledge that the ORI file only contains
JPEG images means that the "RAW DNG" output is not, by any possible meaning of the word, RAW in any way, shape, or form.

Such a processing workflow means that there is no possibility of proper color management (for the recommended color management pipeline
for raw data, see Section 6 of the Adobe DNG Specfication at https://www.adobe.com/content/dam/acom/en/products/photoshop/pdfs/dng_spec_1.4.0.0.pdf

As such, at least as of the time of the writing of this script, this camera is NOT recommended for use, especially not professional use,
due a combination of the proprietary file format and the fact that the proprietary format only contains JPEG images.

If you are asking - where's the EXIF?  The ORI file stores metadata in an unknown fully proprietary arrangement, and as a result this metadata cannot
be extracted and written out as EXIF.  The files within the ORI are JFIF images, not EXIF images (yes, there IS a difference! -
most people don't realize that because an EXIF image is named .jpg and almost universally only stores JPEG data and thus is almost
indistinguishable from metadata-less JFIF other than the lack of metadata.)

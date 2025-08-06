import diplib as dip
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd


def norm(i):
	mn = i.min()
	mx = i.max()
	mx -= mn
	i = ((i-mn)/mx) * 255
	return i.astype(np.uint8)


av = dip.ImageRead('images/2.png')
gf = dip.ColorSpaceManager.Convert(av, 'RGB')
#ff=norm(gf)
#print(ff)
a = dip.ColorSpaceManager.Convert(gf, 'grey')
print(a)
print(gf)
a.SetPixelSize(1, "um")  # "um" is easier to type than "μm", but they mean the same things
b = a < 120
b = dip.EdgeObjectsRemove(b)
b = dip.Label(b, minSize=30)
m = dip.MeasurementTool.Measure(b, a, ['Size', 'Solidity', 'Statistics'])
selection = m['Size'] > 200
sm = m['Solidity'] > 0.9
#selection.Relabel()  # optional
large_object_image = selection.Apply(b)
print(large_object_image)
large_object_image.Show('labels')
plt.show()
#df = m.ToDataFrame()
#print(df)
cc = np.array(large_object_image).astype(np.uint8) * 255
#transo = np.transpose(cc)


cv2.imwrite("images/transposed.png",cc)

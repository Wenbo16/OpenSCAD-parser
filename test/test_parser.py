data3 = '''
TotalWidth = dxf_dim(file="drawing.dxf", name="TotalWidth", layer="SCAD.Origin", origin=[0, 0], scale=1);
'''

data4 = '''
 for(i=[0:36])
    translate([i*10,0,0])
       cylinder(r=5,h=cos(i*10)*50+60);
'''


data6 = '''
linear_extrude(height = 60, twist = 90, slices = 60) {
  difference() {
    offset(r = 10) {
      square(20, center = true);
    }
    offset(r = 8) {
      square(20, center = true);
    }
  }
}

'''

data7 = '''
seed=42;
random_vect=rands(5,15,4,seed);
echo( "Random Vector: ",random_vect);
sphere(r=5);
for(i=[0:3]) {
 rotate(360*i/4) {
   translate([10+random_vect[i],0,0])
     sphere(r=random_vect[i]/2);
 }
}
'''
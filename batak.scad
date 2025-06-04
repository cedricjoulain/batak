include <./F1inter.scad>

$fn=36;//*6
h = 8;
anchorpos = 25;
grooves = 0; // must be = 0 modulo 4 (10 is ok)

module button() difference() {
    cylinder(h=2, r=30, center = true);
    cylinder(h=4, r=25/2+0.5, center = true);
};

module button_hole() union() {
    rotate([0, 0, 75])
    translate([37/2, 0, 0])
    cylinder(h=4, r=2+0.5, center = true);
    rotate([0, 0, 75])
    translate([-37/2, 0, 0])
    cylinder(h=4, r=2+0.5, center = true);
};

// 4/2 hexagon radius 
apothem = 4/2 * sqrt(3)/2;
aspace = 2*apothem;
module hexa_hole() union() {
cylinder(100, r=4/2, center = true, $fn=6);
}

module bolt() union() {
cylinder(16, r=4.5/2, center = true);
translate([0, 0, 6])
cylinder(4, r=8/2, center = true);
};

module top_end()
difference() {
    union() {
        /*
        translate([0, 0, -29])
        tyre(grooves);
        translate([2*60, 0, -29])
        tyre(grooves);*/
        translate([2*60+10, 0, 0])
        button();
        button();
        translate([60+5, 0, 0])
        cube([80, 60, 2], center = true);
        translate([60, 22.5, 0])
        cube([2*60+10, 15, 2], center = true);
        translate([60, -22.5, 0])
        cube([2*60+10, 15, 2], center = true);
    }
    translate([60+5, 0, 0])
    cube([48+2, 20+2, 26], center=true);
    button_hole();
    translate([2*60+10, 0, 0])
    button_hole();
    translate([-50, 0, 0])
    cube([100, 100, 10], center=true);
    translate([anchorpos, anchorpos,-4])
    bolt();
    translate([anchorpos, -anchorpos,-4])
    bolt();
    translate([2*60+10-anchorpos, anchorpos,-4])
    bolt();
    translate([2*60+10-anchorpos, -anchorpos,-4])
    bolt();
};

module logo_serli() {
    translate([67, 14, 1])
    scale([1/7, 1/7, 1/128])
    rotate([0, 0, 180])
    surface(file = "images/serli-logo.png", center = true);
};

module top_middle()
difference() {
    union() {
        translate([2*60+10, 0, 0])
        button();
        button();
        translate([60+5, 0, 0])
        cube([80, 60, 2], center = true);
        translate([60, 22.5, 0])
        cube([2*60+10, 15, 2], center = true);
        translate([60, -22.5, 0])
        cube([2*60+10, 15, 2], center = true);
    }
    logo_serli();
    button_hole();
    translate([2*60+10, 0, 0])
    button_hole();
    translate([-50, 0, 0])
    cube([100, 100, 10], center=true);
    translate([2*60+10+50, 0, 0])
    cube([100, 100, 10], center=true);
    translate([anchorpos, anchorpos,-4])
    bolt();
    translate([anchorpos, -anchorpos,-4])
    bolt();
    translate([2*60+10-anchorpos, anchorpos,-4])
    bolt();
    translate([2*60+10-anchorpos, -anchorpos,-4])
    bolt();
    for(x = [-4:1:4]) {
        for(y = [-27.5: aspace +1 :-6]){
            translate([60 + 5+x*(2*aspace), y, 0])
            hexa_hole();
        }
        for(y = [-27.5: aspace+1:-6]){
            translate([60 + 5+x*(2*aspace)+aspace, y+(aspace/2)+0.5, 0])
            hexa_hole();
        }
    }
};
module anchor(nohole)
difference() {
  if(nohole) {
    cube([10, 10, 29], center=true);
  } else {
    cube([10, 10, 25], center=true);
  }
  if (!nohole) {
    translate([0, 0, 6])
    cylinder(25, r=4.2/2, center = true);
  }
};

module foot(end) union(){
difference() {
 translate([0, 0, -29])
 tyre(grooves);
 cylinder(1000, r=55/2, center = true);
 translate([0, 0, -12])
 cube([100, 61, 28], center=true);
 };
if (end) {
    difference() {
    intersection() {
       translate([0, 0, -29])
       tyre(grooves);
       union() {
         translate([anchorpos, anchorpos,-13.6])
         anchor(true);
         translate([anchorpos, anchorpos+2,-13.6])
         anchor(true);
         translate([anchorpos, -anchorpos,-13.6])
         anchor(true);
         translate([anchorpos, -anchorpos-2,-13.6])
         anchor(true);
       }
      }
      cylinder(4, r=61/2, center = true);     
    }
} else {
  translate([anchorpos, anchorpos,-13.6])
  anchor();
  translate([anchorpos, -anchorpos,-13.6])
  anchor();
}
translate([-anchorpos, anchorpos,-13.6])
rotate([0, 0, 180])
anchor();
translate([-anchorpos, -anchorpos,-13.6])
rotate([0, 0, 180])
anchor();
translate([0, 0,-58])
if (grooves > 0) difference() {
  cylinder(h=2, r=61/2, center = true);
  translate([0,0, -1.5])
  scale([-1/10, 1/10, 1/100])
  surface(file = "images/strigi-logo.png", center = true);
  }
}
// top right rpi foot
module rpi_foot() union() {
  translate([36, -30+6, (20/2)-1])
  cylinder(20, r=3.5, center = true);
  translate([36, -30+6, (25/2)-1])
  cylinder(25, r=1.9/2, center = true);
}

module down_middle()
union() {
difference() {
    union() {
        translate([60+5, 0, 0]) {
          cube([80, 60, 2], center = true);
          translate([0, 0, 12])
          difference() {
              cube([79+50, 60, 24], center = true);
              translate([0, 0, 20])
              scale([1, 1, 1.75])
              rotate([0, 90, 0])
              cylinder(150, r=57/2, center = true);
          }
        }
        translate([60, 22.5, 0])
        cube([2*60+10, 15, 2], center = true);
        translate([60, -22.5, 0])
        cube([2*60+10, 15, 2], center = true);
    }
    translate([-50, 0, 0])
    cube([100, 100, 10], center=true);
    translate([2*60+10+50, 0, 0])
    cube([100, 100, 10], center=true);
    for(x = [-4:1:4]) {
        for(y = [-27.5: aspace +1 :-6]){
            translate([60 + 5+x*(2*aspace), y, 0])
            hexa_hole();
        }
        for(y = [-27.5: aspace+1:-6]){
            translate([60 + 5+x*(2*aspace)+aspace, y+(aspace/2)+0.5, 0])
            hexa_hole();
        }
    }
    translate([anchorpos, anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([anchorpos, -anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    cylinder(1000, r=50/2, center = true);

    translate([2*60+10-anchorpos, anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([2*60+10-anchorpos, -anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([2*60+10, 0, 0])
    cylinder(1000, r=50/2, center = true);
    translate([36-3.5+12.4, -50, 4+21])
    cube([15, 100, 10], center=true);    
    translate([36-3.5+54, -50, 4+21])
    cube([10, 100, 10], center=true);
    // just some space not an hole    
    translate([36-3.5+41.4, -24.4, 4+21])
    cube([10, 10, 10], center=true);    
}
rpi_foot();
translate([58, 0, 0])
rpi_foot();
translate([0, 23, 0])
rpi_foot();
translate([58, 23, 0])
rpi_foot();
};

module down_end()
union() {
difference() {
    union() {
        translate([60+5, 0, 0]) {
          cube([80, 60, 2], center = true);
          translate([0, 0, 12])
          difference() {
              cube([79+50, 60, 24], center = true);
              translate([0, 0, 20])
              scale([1, 1, 1.75])
              rotate([0, 90, 0])
              cylinder(150, r=57/2, center = true);
          }
        }
        translate([60, 22.5, 0])
        cube([2*60+10, 15, 2], center = true);
        translate([60, -22.5, 0])
        cube([2*60+10, 15, 2], center = true);
    }
    translate([-49.5, 0, 0])
    cube([100, 100, 10], center=true);
    for(x = [-4:1:4]) {
        for(y = [-20: aspace +1 :20]){
            translate([60 + 5+x*(2*aspace), y, 0])
            hexa_hole();
        }
        for(y = [-20: aspace+1:20]){
            translate([60 + 5+x*(2*aspace)+aspace, y+(aspace/2)+0.5, 0])
            hexa_hole();
        }
    }
    translate([anchorpos, anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([anchorpos, -anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    cylinder(1000, r=50/2, center = true);

    translate([2*60+10-anchorpos, anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([2*60+10-anchorpos, -anchorpos,0])
    cube([10.5, 10.5, 100], center=true);

    translate([2*60+10, 0, 0])
    cylinder(1000, r=50/2, center = true);
}
// screen support
translate([60+5, (12+36)/2, (21/2)-1])
cube([60, 12, 21], center=true);
translate([60+5, -(12+36)/2, (21/2)-1])
cube([60, 12, 21], center=true);
};


module down_end_black()
difference() {
    union() {
        translate([130, 0, 25])
        difference() {
        intersection() {
          difference() {
            translate([0, 0, -29])
            tyre(grooves);
            cylinder(1000, r=55/2, center = true);
          }
          translate([49.5, 0, -1])
          cube([100, 60, 50], center=true);
         }
         translate([0, 0, 1])
         cylinder(4, r=61/2, center =true);
        }
    }

    translate([2*60+10+anchorpos, anchorpos,0])
    cube([10.5, 10.5, 100], center=true);
    translate([2*60+10+anchorpos, -anchorpos,0])
    cube([10.5, 10.5, 100], center=true);

    translate([2*60+10, 0, 0])
    cylinder(1000, r=50/2, center = true);
};

//logo_serli();
//top_middle();
//foot();
//down_end_black();
down_end();
/*
translate([0, 0, -25])
down_middle();
foot();
translate([130, 0, 0])
foot();
rotate([0, 0, 180]) {
  top_end();
  translate([0, 0, -25])
  down_end();
  translate([2*60+10, 0, 0])
  foot(true);
};
translate([130, 0, 0]) {
  top_end();
  translate([0, 0, -25])
  down_end();
  translate([2*60+10, 0, 0])
  foot(true);
};
*/

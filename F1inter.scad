// variables
$fn=36;
fs = 1.2;  // roughly the size of straight parts of curves
w1 = 2;   // thicker side
w2 = 2;   // thinner side
h = 8;     // height
hh = 80;     // hole height

// points 
p1 = [752-804, 657-657];
p1b = [752-804, 691-657];
p2a = [780-804, 701-657];
p2 = [802-804, 704-657];
p2b = [824-804, 698-657];
p3a = [845-804, 690-657];
p3 = [856-804, 656-657];
p3b = [931-804, 483-657];
p4a = [949-804, 365-657];
p4 = [1006-804, 350-657];
p5 = [1224-804, 310-657];

module tyre(grooves)
union() {
difference() {
    slick();
    if(grooves != 0) {
        step = 360/grooves;
        for ( a = [0:step:360-step]) {
            rotate([ 0, 0, a])
            inter_hole();
            rotate([0, 0, a+step/2])
            scale([1, 1, -1])
            inter_hole();
        }
    }
}
scale([1, 0.9, 1])
slick();
}
// model
module inter_hole()
rotate([0, 90, 0])
union() {
  b_curve(s([p1, p1b, p2a, p2]));
  b_curve(s([p2, p2b, p3a, p3]));
  b_curve(s([p3, p3b, p4a, p4]));
  b_curve(s([p4, p5]));
};

module slick()
rotate_extrude(){
translate([30, 30-8, 0])
scale([1, h/10, 1])
circle(r=10);
translate([30, -(30-8), 0])
scale([1, h/10, 1])
circle(r=10);
translate([34, 0, 0])
scale([1, 2.9, 1])
circle(r=10);
};


// functions and modules
function s(a) = a/15;

function fn(a, b) = round(sqrt(pow(a[0]-b[0],2) + pow(a[1]-b[1], 2))/fs);

function with_slope(p, x_diff, s) // point, difference in x, slope
    = [p[0] + x_diff, p[1] + x_diff * s];    

module shape() cylinder(hh, w1/2, w2/2, $fn=12);
    
module b_curve(pts)             // pts is an array of points
    let (idx=fn(pts[0], pts[len(pts)-1]), n = 1/idx){       
        for (i= [0:idx-1]) 
        hull(){ 
           translate(b_pts(pts, n, i)) shape();
           translate(b_pts(pts, n, i+1)) shape();          
        }
    }
    
function b_pts(pts, n, idx) =       // gets called by b_curve() ...
    len(pts)>2 ?                    // ... and b_curve_rainbow() 
        b_pts([for(i=[0:len(pts)-2])pts[i]], n, idx) * n*idx 
            + b_pts([for(i=[1:len(pts)-1])pts[i]], n, idx) * (1-n*idx)
        : pts[0] * n*idx 
            + pts[1] * (1-n*idx);

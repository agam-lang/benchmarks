fn ray_sphere_intersect(
    ray_ox: f64, ray_oy: f64, ray_oz: f64,
    ray_dx: f64, ray_dy: f64, ray_dz: f64,
    sp_x: f64, sp_y: f64, sp_z: f64, sp_r: f64
) -> f64 {
    let oc_x = ray_ox - sp_x;
    let oc_y = ray_oy - sp_y;
    let oc_z = ray_oz - sp_z;

    let b = oc_x * ray_dx + oc_y * ray_dy + oc_z * ray_dz;
    let c = oc_x * oc_x + oc_y * oc_y + oc_z * oc_z - sp_r * sp_r;
    let disc = b * b - c;

    if disc < 0.0 {
        return -1.0;
    }
    -b - 1.0
}

fn render_scene(rays_per_pixel: usize, width: usize, height: usize) -> i32 {
    let mut hit_count = 0;
    for y in 0..height {
        for x in 0..width {
            for _ in 0..rays_per_pixel {
                let dx = (x as f64 - (width as f64 / 2.0)) / (width as f64);
                let dy = (y as f64 - (height as f64 / 2.0)) / (height as f64);
                let dz = 1.0;

                let t = ray_sphere_intersect(0.0, 0.0, -5.0, dx, dy, dz, 0.0, 0.0, 0.0, 2.0);
                if t > 0.0 {
                    hit_count += 1;
                }
            }
        }
    }
    hit_count
}

fn main() {
    let hits = render_scene(16, 128, 128);
    println!("{}", hits);
}

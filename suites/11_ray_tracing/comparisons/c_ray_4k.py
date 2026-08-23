def ray_sphere_intersect(ray_ox, ray_oy, ray_oz, ray_dx, ray_dy, ray_dz, sp_x, sp_y, sp_z, sp_r):
    oc_x = ray_ox - sp_x
    oc_y = ray_oy - sp_y
    oc_z = ray_oz - sp_z

    b = oc_x * ray_dx + oc_y * ray_dy + oc_z * ray_dz
    c = oc_x * oc_x + oc_y * oc_y + oc_z * oc_z - sp_r * sp_r
    disc = b * b - c

    if disc < 0.0:
        return -1.0
    return -b - 1.0

def render_scene(rays_per_pixel, width, height):
    hit_count = 0
    for y in range(height):
        for x in range(width):
            for _ in range(rays_per_pixel):
                dx = (x - (width / 2.0)) / width
                dy = (y - (height / 2.0)) / height
                dz = 1.0

                t = ray_sphere_intersect(0.0, 0.0, -5.0, dx, dy, dz, 0.0, 0.0, 0.0, 2.0)
                if t > 0.0:
                    hit_count += 1
    return hit_count

def main():
    hits = render_scene(16, 128, 128)
    print(hits)

if __name__ == "__main__":
    main()

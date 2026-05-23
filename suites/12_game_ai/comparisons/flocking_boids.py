def flocking_boids(boids: int) -> int:
    checksum = 0
    frames = 30
    
    for f in range(frames):
        center_mass_sum = 0
        for i in range(boids):
            px = (i * 17 + f * 7) % 1000
            py = (i * 19 + f * 11) % 1000
            vx = ((i * 23) % 20) - 10
            vy = ((i * 29) % 20) - 10
            
            sep_x, sep_y, align_x, align_y, coh_x, coh_y = 0, 0, 0, 0, 0, 0
            neighbors = 0
            
            for j in range(boids):
                if i != j:
                    ox = (j * 17 + f * 7) % 1000
                    oy = (j * 19 + f * 11) % 1000
                    ovx = ((j * 23) % 20) - 10
                    ovy = ((j * 29) % 20) - 10
                    
                    dx, dy = px - ox, py - oy
                    dist_sq = dx*dx + dy*dy
                    
                    if dist_sq < 2500:
                        neighbors += 1
                        if dist_sq < 400:
                            sep_x += dx
                            sep_y += dy
                        align_x += ovx
                        align_y += ovy
                        coh_x += ox
                        coh_y += oy
            
            new_vx, new_vy = vx, vy
            if neighbors > 0:
                align_x = (align_x // neighbors) - vx
                align_y = (align_y // neighbors) - vy
                coh_x = (coh_x // neighbors) - px
                coh_y = (coh_y // neighbors) - py
                
                new_vx = vx + (sep_x * 5 + align_x * 2 + coh_x * 1) // 100
                new_vy = vy + (sep_y * 5 + align_y * 2 + coh_y * 1) // 100
            center_mass_sum = (center_mass_sum + new_vx + new_vy) % 1000000007
        checksum = (checksum * 31 + center_mass_sum) % 1000000007
    return checksum

if __name__ == "__main__":
    print(flocking_boids(512))

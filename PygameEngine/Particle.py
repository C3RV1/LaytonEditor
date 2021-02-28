import PygameEngine.Sprite
import PygameEngine.GameManager
import PygameEngine.Screen


class Particle(PygameEngine.Sprite.Sprite):
    def __init__(self, groups, vel=(0, 0), accel=(0, 0), alive_time=0.001, frame_delay=0.001, use_sprite_time=False):
        PygameEngine.Sprite.Sprite.__init__(self, groups)
        self.vel = list(vel)
        self.accel = list(accel)
        self.alive_time = alive_time
        self._current_alive_time = 0
        self._current_frame_time = 0
        self.frame_delay = frame_delay
        self.gm = PygameEngine.GameManager.GameManager()

        self.use_sprite_time = use_sprite_time

    def update_particle(self):
        self._current_alive_time += self.gm.delta_time
        self._current_frame_time += self.gm.delta_time
        if self._current_alive_time >= self.alive_time:
            self.kill()
            return False
        self.update_frame_delay()
        while self._current_frame_time > self.frame_delay:
            self._current_frame_time -= self.frame_delay
            self.frame = self.frame + 1
            self.frame = min(self.frame, self.frame_count - 1)
            self._update_frame_info()
            self.update_frame_delay()
        self.update_frame()
        self.vel[0] += self.accel[0] * self.gm.delta_time
        self.vel[1] += self.accel[1] * self.gm.delta_time
        self.world_rect[0] += self.vel[0] * self.gm.delta_time
        self.world_rect[1] += self.vel[1] * self.gm.delta_time
        return True

    def update_frame_delay(self):
        if self.use_sprite_time:
            self.frame_delay = self.duration


class ParticleEmitter(PygameEngine.Sprite.Sprite):
    def __init__(self, groups, particle_time=0, new_particle_func=None):
        PygameEngine.Sprite.Sprite.__init__(self, groups)
        self.particles = []
        self.new_particle_lambda = new_particle_func
        self.particle_time = particle_time
        self._current_particle_time = 0
        self.screen_size = PygameEngine.Screen.Screen.screen_size()
        self.gm = PygameEngine.GameManager.GameManager()

    def check_on_view(self):
        if self.rect[0] < -100 or self.rect[0] > self.screen_size[0] + 100:
            return False
        if self.rect[1] < -100 or self.rect[1] > self.screen_size[1] + 100:
            return False
        return True

    def update(self):
        if self.check_on_view() and callable(self.new_particle_lambda):
            self._current_particle_time += self.gm.delta_time

            while self._current_particle_time > self.particle_time > 0:
                new_particle = self.new_particle_lambda(self)
                self.particles.append(new_particle)
                self._current_particle_time -= self.particle_time
        particles_to_remove = []
        for particle in self.particles:
            particle: Particle
            if not particle.update_particle():
                particles_to_remove.append(particle)
        for particle in particles_to_remove:
            self.particles.remove(particle)

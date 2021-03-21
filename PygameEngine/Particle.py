from .Sprite import Sprite
from .GameManager import GameManager
from .Screen import Screen


class Particle(Sprite):
    def __init__(self, groups, vel=(0, 0), accel=(0, 0), alive_time=0.001, frame_delay=0.001, use_sprite_time=False):
        Sprite.__init__(self, groups)
        self.vel = list(vel)
        self.accel = list(accel)
        self.alive_time = alive_time
        self._current_alive_time = 0
        self._current_frame_time = 0
        self.frame_delay = frame_delay
        self.gm = GameManager()

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
            self.frame_num = self.frame_num + 1
            self.frame_num = min(self.frame_num, self.frame_count - 1)
            self.update_frame_delay()
        self.update_frame()
        self.vel[0] += self.accel[0] * self.gm.delta_time
        self.vel[1] += self.accel[1] * self.gm.delta_time
        self.world_rect[0] += self.vel[0] * self.gm.delta_time
        self.world_rect[1] += self.vel[1] * self.gm.delta_time
        return True

    def update_frame_delay(self):
        if self.use_sprite_time and self.is_sprite_sheet:
            self.frame_delay = self.sprite_sheet_info["frames"][self.frame_num]["duration"]


class ParticleEmitter(Sprite):
    def __init__(self, groups, particle_time=0, particle_factory=None):
        Sprite.__init__(self, groups)
        self.particles = []
        self.particle_factory = particle_factory
        self.particle_time = particle_time
        self._current_particle_time = 0
        self.screen_size = Screen.screen_size()
        self.gm = GameManager()
        self.active = True

    def check_on_view(self):
        if self.rect.w <= 0:
            return False
        if self.rect.h <= 0:
            return False
        return True

    def update(self):
        if self.check_on_view() and callable(self.particle_factory):
            self._current_particle_time += self.gm.delta_time

            while self._current_particle_time > self.particle_time > 0:
                if self.active:
                    new_particle = self.particle_factory(self)
                    self.particles.append(new_particle)
                self._current_particle_time -= self.particle_time
        particles_to_remove = []
        for particle in self.particles:
            if not isinstance(particle, Particle):
                particles_to_remove.append(particle)
                continue
            particle: Particle
            if not particle.update_particle():
                particles_to_remove.append(particle)
        for particle in particles_to_remove:
            self.particles.remove(particle)

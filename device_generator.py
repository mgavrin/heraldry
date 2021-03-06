import os
import pygame
from pygame.locals import *

constant_definitions =open("constants.py")
exec(constant_definitions.read())


class Device:
    def __init__(self, blazon = "", field_sections = [], charge_groups = []):
        '''
        Set either a blazon or a list of field_sections and a list of charge_groups.
        blazon: a string description to attempt to parse.
        field_sections: a list of FieldSection objects.
        charge_groups: a list of ChargeGroup objects.
        '''

        size = (kScreenWidth, kScreenHeight)
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.screen.fill(kGrey)

        if blazon and (field_sections or charge_groups):
            print("Error: cannot use both blazon and manual field/charges.")
        elif not blazon and not field_sections:
            print("Error: at least one field division is required. It can be just a plain tincture.")

        if blazon != "":
            #TODO implement blazon parsing
            print ("Sorry, blazon parsing isn't supported yet.")
            self.field_sections = []
            self.charge_groups = []
        else:
            self.field_sections = field_sections
            self.charge_groups = charge_groups

    def display_device(self):
        '''
        Displays a single device until the user changes it. Right now all the user can do is quit.
        field_sections: a list of Field instances, representing portions of the field.
        charge_groups: a list of ChargeGroup instances, representing charge groups 
        (which can be a single charge, a set of the same or different charges, or a charge with tertiary charges on it).
        '''
        for section in self.field_sections:
            section.surface.lock
            section.mask.lock
            self.screen.lock
            for x in range(kScreenWidth):
                for y in range(kScreenHeight):
                    if section.mask.get_at((x,y)) == kGrey:
                        self.screen.set_at((x,y),
                                           section.surface.get_at((x,y)))
        for charge in self.charge_groups:
            pass
            #charge.draw_charge()
            
        # Add the shield outline
        shield_mask = pygame.transform.scale(
            pygame.image.load(os.path.join("art", "shield mask vector.png")),
            (kScreenWidth, kScreenHeight))
        self.screen.blit(shield_mask, [0,0])

        # Flip the screen to update changes
        pygame.display.flip()

        while True:
            events=pygame.event.get()
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                if event.type==QUIT:
                    pygame.display.quit()
                    return

    def merge(self, other):
        self.field_sections+=other.field_sections
        self.charge_groups+=other.charge_groups

class FieldSection:
    def __init__(self, surface, mask):
        '''
        surface: a pygame Surface object the size of the screen containing some tincture or fur.
        mask: a pygame Surface object the size of the screen containing 
          grey pixels where the surface should be visible
          and white pixels elsewhere. Black pixels need not be contiguous.
        '''
        self.surface = surface
        self.mask = mask

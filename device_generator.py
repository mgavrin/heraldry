import os
import pygame
from pygame.locals import *

kArgent = (255, 255, 255)
kOr = (255, 255, 0)
kSable = (0, 0, 0)
kGules = (255, 0, 0)
kVert = (0, 255, 0)
kAzure = (0, 0, 255)
kPurpure = (150, 50, 255)
kScreenWidth = 1000
kScreenHeight = 1000

class Device:
    def __init__(self, blazon = "", field_sections = [], charge_groups = []):
        '''
        Set either a blazon or a list of field_sections and a list of charge_groups.
        blazon: a string description to attempt to parse.
        field_sections: a list of FieldSection objects.
        charge_groups: a list of ChargeGroup objects.
        '''
        self.Margin = int(kScreenWidth/20)
        self.ShieldCurveTop = int(kScreenHeight/2)
        self.ShieldBottomPoint = int(kScreenHeight*875/1000)
        self.CtrlPt1 = 650
        self.CtrlPt2X = 425
        self.CtrlPt2Y = 880

        size = (kScreenWidth, kScreenHeight)
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.screen.fill((176,176,176))

        if blazon and (field_sections or charge_groups):
            print("Error: cannot use both blazon and manual field/charges.")
        elif not blazon and not field_sections:
            print("Error: at least one field division is required. It can be just a plain tincture.")

        if blazon != "":
            #TODO unfake this
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
            field_section_surface = section.draw_field_section()
            # Blit at [0,0] because positioning is handled in the FieldSection object
            self.screen.blit(field_section_surface, [0,0])
        for charge in self.charge_groups:
            pass
            #charge.draw_charge()
        # Add the shield outline
        shield_mask = pygame.transform.scale(
            pygame.image.load(os.path.join("art", "shield mask.png")),
            (kScreenWidth, kScreenHeight))
        self.screen.blit(shield_mask, [0, 0])

        # Flip the screen to update changes
        pygame.display.flip()

        while True:
            events=pygame.event.get()
            for event in events:
                if event.type==QUIT:
                    pygame.display.quit()
                    return

class FieldSection:
    def __init__(self, boundary_points, tincture = None, fur = None):
        '''
        boundary_points: coordinates of the vertices of the field division on the full screen
        tincture: kAzure or kGules or similar
        fur: a Fur object
        Do not set both tincture and fur. Possibly I will change my mind about this structure when I implement barry/pally/etc.
        '''
        self.boundary = boundary_points
        self.tincture = tincture
        self.fur = fur
        if tincture != None and fur != None:
            print("Do not attempt to put a tincture and a fur on the same part of the field.")

    def draw_field_section(self):
        return_surface = pygame.Surface((kScreenWidth, kScreenHeight), pygame.SRCALPHA) #SRCALPHA ensures surface initializes transparent
        if self.tincture:
            pygame.draw.polygon(return_surface, self.tincture, self.boundary)
        else:
            pass #handle furs once you have a Fur class
        #TODO decide whether to locate the section on the shield here or in Device
        return return_surface

#TODO: when you get to parsing, put all these boundary boxen in a library of constants and import it.
'''
full_field = [[0, 0], [0, kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
azure = Device("", [FieldSection(full_field, kAzure)])
azure.display_device()

dexter_half_boundary = [[0, 0], [0, kScreenHeight], [int(kScreenWidth/2), kScreenHeight], [int(kScreenWidth/2), 0]]
sinister_half_boundary = [[int(kScreenWidth/2), 0], [int(kScreenWidth/2), kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, 0]]
dexter_azure = FieldSection(dexter_half_boundary, kAzure)
sinister_or = FieldSection(sinister_half_boundary, kOr)
per_pale = Device("", [dexter_azure, sinister_or])
per_pale.display_device()

chief_half_boundary = [[0, 0], [0, int(kScreenHeight*5/12)], [kScreenWidth, int(kScreenHeight*5/12)], [kScreenWidth, 0]]
base_half_boundary = [[0, int(kScreenHeight*5/12)], [0, kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, int(kScreenHeight*5/12)]]
chief_gules = FieldSection(chief_half_boundary, kGules)
base_argent = FieldSection(base_half_boundary, kArgent)
per_fess = Device("", [chief_gules, base_argent])
per_fess.display_device()

dexter_chief_boundary = [[0, 0], [0, kScreenHeight], [int(kScreenWidth*.97), 0]]
sinister_base_boundary = [[0, kScreenHeight], [int(kScreenWidth*.97), kScreenHeight], [int(kScreenWidth*.97), 0]]
dexter_chief_purpure = FieldSection(dexter_chief_boundary, kPurpure)
sinister_base_argent = FieldSection(sinister_base_boundary, kArgent)
per_bend = Device("", [dexter_chief_purpure, sinister_base_argent])
per_bend.display_device()

sinister_chief_boundary = [[int(kScreenWidth*.03), 0], [kScreenWidth, 0], [kScreenWidth, kScreenHeight]]
dexter_base_boundary = [[int(kScreenWidth*.03), 0], [int(kScreenWidth*.03), kScreenHeight], [kScreenWidth, kScreenHeight]]
sinister_chief_purpure = FieldSection(sinister_chief_boundary, kPurpure)
dexter_base_argent = FieldSection(dexter_base_boundary, kArgent)
per_bend_sinister = Device("", [sinister_chief_purpure, dexter_base_argent])
per_bend_sinister.display_device()

dexter_chief_quarter = [[0, 0], [0, int(kScreenHeight*5/12)], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth/2), 0]]
sinister_chief_quarter = [[int(kScreenWidth/2), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [kScreenWidth, int(kScreenHeight*5/12)], [kScreenWidth, 0]]
dexter_base_quarter = [[0, int(kScreenHeight*5/12)], [0, kScreenHeight], [int(kScreenWidth/2), kScreenHeight], [int(kScreenWidth/2), int(kScreenHeight*5/12)]]
sinister_base_quarter = [[int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth/2), kScreenHeight], [kScreenWidth, kScreenHeight], [kScreenWidth, int(kScreenHeight*5/12)]]
dexter_chief_gules = FieldSection(dexter_chief_quarter, kGules)
sinister_chief_argent = FieldSection(sinister_chief_quarter, kArgent)
dexter_base_argent = FieldSection(dexter_base_quarter, kArgent)
sinister_base_gules = FieldSection(sinister_base_quarter, kGules)
quarterly = Device("", [dexter_chief_gules, sinister_chief_argent, dexter_base_argent, sinister_base_gules])
quarterly.display_device()
'''

chief_saltire_boundary = [[int(kScreenWidth*.03), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), 0]]
dexter_saltire_boundary = [[int(kScreenWidth*.03), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.03), int(kScreenHeight*10/12)]]
# There are four points here. Don't mess with this without looking at it really carefully first.
base_saltire_boundary = [[int(kScreenWidth*.03), int(kScreenHeight*10/12)], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), int(kScreenHeight*10/12)], [int(kScreenWidth/2), kScreenHeight]]
sinister_saltire_boundary = [[int(kScreenWidth*.97), 0], [int(kScreenWidth/2), int(kScreenHeight*5/12)], [int(kScreenWidth*.97), int(kScreenHeight*10/12)]]
chief_saltire_section = FieldSection(chief_saltire_boundary, kArgent)
dexter_saltire_section = FieldSection(dexter_saltire_boundary, kPurpure)
base_saltire_section = FieldSection(base_saltire_boundary, kArgent)
sinister_saltire_section = FieldSection(sinister_saltire_boundary, kPurpure)
per_saltire = Device("", [chief_saltire_section, dexter_saltire_section, base_saltire_section, sinister_saltire_section])
per_saltire.display_device()

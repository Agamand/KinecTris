# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Delicode NI mate",
    "author": "Janne Karhu (jahka)",
    "version": (1, 0),
    "blender": (2, 6, 1),
    "api": 35622,
    "location": "Toolbar > Delicode NI mate",
    "description": "Receives OSC data from the Delicode NI mate program",
    "category": "Animation",
    'wiki_url': '',
    'tracker_url': ''
    }

from mathutils import Vector

import math
import struct

try:
    import bge
    GE = True
except ImportError:
    GE = False
    import bpy
    from bpy.props import *
    
import socket

def set_GE_data(objects, ob_name, vec):
    ob = objects.get(ob_name)
    
    if ob != None:
        ob.localPosition = Vector([vec[0]*10, -vec[2]*10, vec[1]*10])

def set_data(objects, ob_name, vec):
    if ob_name in objects.keys():
        objects[ob_name].location = Vector([vec[0]*10, -vec[2]*10, vec[1]*10])
        
        if(bpy.context.scene.tool_settings.use_keyframe_insert_auto):
            objects[ob_name].keyframe_insert(data_path="location")
            
class OSC():
    def readByte(data):
    	length   = data.find(b'\x00')
    	nextData = int(math.ceil((length+1) / 4.0) * 4)
    	return (data[0:length], data[nextData:])

    
    def readString(data):
        length   = str(data).find("\0")
        nextData = int(math.ceil((length+1) / 4.0) * 4)
        return (data[0:length], data[nextData:])
    
    
    def readBlob(data):
        length   = struct.unpack(">i", data[0:4])[0]
        nextData = int(math.ceil((length) / 4.0) * 4) + 4
        return (data[4:length+4], data[nextData:])
    
    
    def readInt(data):
        if(len(data)<4):
            print("Error: too few bytes for int", data, len(data))
            rest = data
            integer = 0
        else:
            integer = struct.unpack(">i", data[0:4])[0]
            rest    = data[4:]
    
        return (integer, rest)
    
    
    def readLong(data):
        """Tries to interpret the next 8 bytes of the data
        as a 64-bit signed integer."""
        high, low = struct.unpack(">ll", data[0:8])
        big = (long(high) << 32) + low
        rest = data[8:]
        return (big, rest)
    
    
    def readDouble(data):
        """Tries to interpret the next 8 bytes of the data
        as a 64-bit double float."""
        floater = struct.unpack(">d", data[0:8])
        big = float(floater[0])
        rest = data[8:]
        return (big, rest)
    
    
    
    def readFloat(data):
        if(len(data)<4):
            print("Error: too few bytes for float", data, len(data))
            rest = data
            float = 0
        else:
            float = struct.unpack(">f", data[0:4])[0]
            rest  = data[4:]
    
        return (float, rest)
    
    def decodeOSC(data):
        table = { "i" : OSC.readInt, "f" : OSC.readFloat, "s" : OSC.readString, "b" : OSC.readBlob, "d" : OSC.readDouble }
        decoded = []
        address,  rest = OSC.readByte(data)
        typetags = ""
        
        if address == "#bundle":
            time, rest = readLong(rest)
            decoded.append(address)
            decoded.append(time)
            while len(rest)>0:
                length, rest = OSC.readInt(rest)
                decoded.append(OSC.decodeOSC(rest[:length]))
                rest = rest[length:]
    
        elif len(rest) > 0:
            typetags, rest = OSC.readByte(rest)
            decoded.append(address)
            decoded.append(typetags)
            
            if len(typetags) > 0:        
                if typetags[0] == ord(','):
                    for tag in typetags[1:]:
                        value, rest = table[chr(tag)](rest)
                        decoded.append(value)
                else:
                    print("Oops, typetag lacks the magic")
    
        return decoded

 
class NImateReceiver():
    def run(self, objects, set_data_func):
        dict = {}
        
        try:
            data = self.sock.recv( 1024 )
        except:
            return {'PASS_THROUGH'}
        
        trash = data
        while(True):
            data = trash
            
            decoded = OSC.decodeOSC(data)
            if(len(decoded) == 5):
                dict[str(decoded[0],"utf-8")] = ([decoded[2], decoded[3], decoded[4]])
            
            try:
                trash = self.sock.recv(1024)
            except:
                break
            
        for key, value in dict.items():
            set_data_func(objects, key, value)


    def __init__(self, UDP_PORT):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(0)
        self.sock.bind( ("localhost", UDP_PORT) )
        
        print("Delicode NI mate Addon started listening to OSC on port " + str(UDP_PORT))
        
    def __del__(self):
        self.sock.close()
        print("Delicode NI mate Addon stopped listening to OSC")
 
if not GE:
    class DelicodeNImate(bpy.types.Operator):
        bl_idname = "wm.delicode_ni_mate_start"
        bl_label = "Delicode NI mate Start"
        bl_options = {'REGISTER'}
        
        enabled = False
        receiver = None
        timer = None
        
        def modal(self, context, event):
            if event.type == 'ESC' or not __class__.enabled:
                return self.cancel(context)
            
            if event.type == 'TIMER':
                self.receiver.run(bpy.data.objects, set_data)
            
            return {'PASS_THROUGH'}     

        def execute(self, context):
            __class__.enabled = True
            self.receiver = NImateReceiver(context.scene.delicode_ni_mate_port)
            
            context.window_manager.modal_handler_add(self)
            self.timer = context.window_manager.event_timer_add(1/context.scene.render.fps, context.window)
            return {'RUNNING_MODAL'}
        
        def cancel(self, context):
            __class__.enabled = False
            context.window_manager.event_timer_remove(self.timer)
            
            del self.receiver
            
            return {'CANCELLED'}
        
        @classmethod
        def disable(cls):
            if cls.enabled:
                cls.enabled = False
                
    class DelicodeNImateStop(bpy.types.Operator):
        bl_idname = "wm.delicode_ni_mate_stop"
        bl_label = "Delicode NI mate Stop"
        bl_options = {'REGISTER'}
        
        def execute(self, context):
            DelicodeNImate.disable()
            return {'FINISHED'}
        
    class VIEW3D_PT_DelicodeNImatePanel(bpy.types.Panel):
        bl_space_type = "VIEW_3D"
        bl_region_type = "TOOLS"
        bl_label = "Delicode NI mate"
        
        def draw(self, context):
            layout = self.layout
            
            scene = context.scene
            
            col = layout.column()
            col.enabled = not DelicodeNImate.enabled
            col.prop(scene, "delicode_ni_mate_port")
            
            if(DelicodeNImate.enabled):
                layout.operator("wm.delicode_ni_mate_stop", text="Stop")
            else:
                layout.operator("wm.delicode_ni_mate_start", text="Start")
        
def init_properties():
    if GE:
        return
        
    scene = bpy.types.Scene
    
    scene.delicode_ni_mate_port = bpy.props.IntProperty(
        name="Port",
        description="Receive OSC on this port",
        default = 7000,
        min = 0,
        max = 65535)
        
def clear_properties():
    if GE:
        return
        
    scene = bpy.types.Scene
    
    del scene.delicode_ni_mate_port
            
def register():
    if GE:
        return
        
    init_properties()
    bpy.utils.register_module(__name__)

def unregister():
    if GE:
        return
        
    bpy.utils.unregister_module(__name__)
    clear_properties()
     
if GE:
    if hasattr(bge.logic, 'DelicodeNImate') == False:
        obj = bge.logic.getCurrentController().owner
        port = obj.get('NImatePort', "")
        if isinstance(port, bool) or not isinstance(port, int):
            print("Add an integer game property 'NImatePort' to the object '" + obj.name + "' to change the Delicode NI mate Addon port.")
            port = 7000
            
        bge.logic.DelicodeNImate = NImateReceiver(port)
        
    bge.logic.DelicodeNImate.run(bge.logic.getCurrentScene().objects, set_GE_data)
elif __name__ == "__main__":
    register()
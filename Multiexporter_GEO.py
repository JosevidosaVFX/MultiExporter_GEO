import os
from PySide2 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        """Create the window type."""
        super().__init__()
        # Head of window.
        self.setWindowTitle("MultiExporter GEO")
        # Size of window.
        self.setMinimumSize(400, 400)
        self.setMaximumSize(800, 800)
        # Margin of Window..
        self.setContentsMargins(10, 10, 10, 10)
        # Layout construction.
        self.build_layout()
                        
    def build_layout(self):
        """Create the window type and widgets types."""
        # MainLayout type assignment.
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Widgets in of Main Layout.
        lst_sop_nodes = self.geo_nodes_selected()
        label_widget = QtWidgets.QLabel(
            f"Selected Geometry Nodes: {len(lst_sop_nodes)}"
            )
        main_layout.addWidget(label_widget)
        # QListWidget obj selected.
        self.list_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.list_widget)
        self.list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
                
        self.list_widget.addItems(lst_sop_nodes)
        
        # Horizontal Layout inside of MainLayout.
        horizontal_1 = QtWidgets.QHBoxLayout()
        # QToolButton in of Horizontal Layout.
        btn = QtWidgets.QToolButton()
        btn.setToolTip("Add Path")
        icon = QtWidgets.QApplication.style().standardIcon(
            QtWidgets.QStyle.SP_DirIcon
        )
        btn.setIcon(QtGui.QIcon(icon))
        horizontal_1.addWidget(btn)
        btn.clicked.connect(self.q_dialog)
        # QLineEdit in of Horizontal Layout.
        self.line_widget = QtWidgets.QLineEdit()
        horizontal_1.addWidget(self.line_widget)               
        main_layout.addLayout(horizontal_1)        
        
        #Vertical Layout inside of MainLayout.
        vertical_1 = QtWidgets.QVBoxLayout()
                
        # QLabel formats.
        file_format_lbl = QtWidgets.QLabel("Select File Format: ")
        vertical_1.addWidget(file_format_lbl)
        
        # QComboBox of format types. 
        self.combo_format = QtWidgets.QComboBox()
        vertical_1.addWidget(self.combo_format)
        self.combo_format.addItems([" ",".FBX",".ABC",".USD"])
        
        self.combo_format.currentTextChanged.connect(self.formats)
      
        # QCheckBox frame range selection.
        self.checkbox = QtWidgets.QCheckBox("Export Animation")
        self.checkbox.setToolTip("Static or Animated")
        vertical_1.addWidget(self.checkbox)
        
        self.checkbox.stateChanged.connect(self.frame_range)
               
        # QPushButton to export files.
        btn = QtWidgets.QPushButton("Export Mesh")
        vertical_1.addWidget(btn)
        main_layout.addLayout(vertical_1)
        btn.clicked.connect(self.exportMesh)  
               
    def q_dialog(self):
        """Select a path and return it"""
        self.dlg = QtWidgets.QFileDialog.getExistingDirectory(self,
            "Choose your export path", "C:"
            )
        # Set the path from self.dlg in line.
        self.line_widget.setText(self.dlg)
              
    def geo_nodes_selected(self):
        """Returns a list of the selected geo nodes and the quantity"""
        sop_nodes = hou.node("/obj")
        
        nodes_selected = sop_nodes.children()
        
        self.list_selected_nodes = []
        for nod_selected in nodes_selected:
            if nod_selected.type().name() == "geo":
                node = nod_selected.name()
                      
                self.list_selected_nodes.append(node)
        self.list_selected_nodes.sort()        
        return self.list_selected_nodes
       
    def list_name(self):
        """Returns the selected names in the QListWidget"""
        selection = self.list_widget.selectedItems()
        self.selected_list = []
        for item in selection:
            self.items = item.text()  
            self.selected_list.append(self.items)
        return self.selected_list
         
    def formats(self, txt):
        """Returns the selected values in the formats of QComboBox"""
        self.format = txt       
        return self.format
        
    def frame_range(self):
        """Checkbox function, analyzes the states of the QCheckBox"""
                     
        if self.checkbox.isChecked():                         
            return 1
            
        else:
            
            return 0            
        
    def exportMesh(self):
        """Export the selected files according to whether they are:
        .fbx, .abc, .usd         
        """
        # Call to other methods.
        path = self.dlg
        name_node = self.list_name()        
        name_format = self.format.lower()          
        frames = self.frame_range()
                       
        for item_selected in name_node:
            
            obj = hou.node(f"/obj/{item_selected}")
            
            for i in obj.children():
                
                if i.isDisplayFlagSet():
                     
                    # Export in .FBX.
                    if name_format == ".fbx":
                        
                        export_node_fbx = i.createOutputNode("rop_fbx")
                    
                        out_path_fbx = export_node_fbx.parm("sopoutput").set(
                            f"{path}/{item_selected}{name_format}"
                            )
                        parm_frames= export_node_fbx.parm("trange").set(frames)
                        export_node_fbx.parm("deformsasvcs").set(1)
                    
                        export_node_fbx.parm("execute").pressButton()                        
                        export_node_fbx.destroy()                        
                        
                    # Export in .ABC.
                    if name_format == ".abc":
                        
                        export_node_abc = i.createOutputNode("rop_alembic")                                                
                    
                        out_path_abc = export_node_abc.parm("filename").set(
                            f"{path}/{item_selected}{name_format}"
                            )
                        parm_frames= export_node_abc.parm("trange").set(frames)
                        
                        export_node_abc.parm("execute").pressButton()
                        export_node_abc.destroy()

                    # Export in .USD.    
                    if name_format == ".usd":
                        
                        export_node_usd = i.createOutputNode("usdexport")
                                                                    
                        out_path_usd = export_node_usd.parm("lopoutput").set(
                            f"{path}/{item_selected}{name_format}"
                            )
                        parm_frames= export_node_usd.parm("trange").set(frames)
                        
                        export_node_usd.parm("execute").pressButton()
                        export_node_usd.destroy()

ui = Window()
ui.show()
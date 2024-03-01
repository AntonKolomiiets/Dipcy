from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QSlider, QFileDialog, QLabel, QWidget, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QPixmap, QImage
import sys
import cv2 as cv
import numpy as np
import os
from scipy.ndimage import gaussian_filter
from Base_GUI import Ui_MainWindow  

#######Dipcy########

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Dipcy")

        self.base_image = None
        self.current_image = None

        self.layer_counter = 0
        self.layers = []
        self.listForCombobox = [stm for stm, value in Edit.__dict__.items() if isinstance(value, staticmethod)]
        #self.listOfFunctions = []
        
        #print(self.listForCombobox)

        self.init_value = 0

    #######BUTTONS########    
        
        self.pushButtonExport.setVisible(False)
        self.openImageButton.clicked.connect(self.main)
        self.button_addLayer.clicked.connect(self.addLayer)
        self.button_removeLayer.clicked.connect(self.removeLayer)
        self.pushButtonExport.clicked.connect(self.export)
        
        self.treeWidgetLayers.currentItemChanged.connect(self.changePage)
        #self.treeWidgetLayers.itemSelectionChanged.connect(lambda: print(self.treeWidgetLayers.selectedItems()[-1].text(0)) if self.treeWidgetLayers.selectedItems() else None)
        self.treeWidgetLayers.itemsReordered.connect(self.applyFunctionsAndShow)



#Open And Display Image
#####################################################

    def main(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        if imagePath:
            self.base_image = cv.imread(imagePath, cv.IMREAD_UNCHANGED).astype(np.float32) / 255
            self.currentFileName = os.path.basename(imagePath)
            self.current_image = self.base_image.copy()
            self.applyFunctionsAndShow()
            self.openImageButton.setVisible(False)
            self.pushButtonExport.setVisible(True)

    def getQPixmapFromImage(self, image):
        if image is not None:
            display_image = (image * 255).astype(np.uint8)
            self.final_image = display_image
            display_image = cv.cvtColor(display_image, cv.COLOR_BGR2RGB)
            height, width, _ = display_image.shape
            bytesPerLine = 3 * width
            qImg = QImage(display_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            
            screenSize = QApplication.primaryScreen().size()
            scaleFactor = 0.5 if max(screenSize.width(), screenSize.height()) > 2000 else 1
            qImg = qImg.scaled(screenSize.width() * scaleFactor, screenSize.height() * scaleFactor, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) #fixed to work?
            
            return QPixmap.fromImage(qImg)
                 
    def applyFunctionsAndShow(self):
        image = self.base_image.copy()
        for index in range(self.treeWidgetLayers.topLevelItemCount()):
            item = self.treeWidgetLayers.topLevelItem(index)
            layer = item.data(0, Qt.UserRole)
            image = layer.function(image, *layer.args, **layer.kwargs)
        self.imageLabel.setPixmap(self.getQPixmapFromImage(image))
        #print("updated")

#####################################################

    def addLayer(self):
        self.layer_counter += 1 #int(self.treeWidgetLayers.topLevelItemCount())
        layer_name = f"Layer {self.layer_counter}"
        new_tree_item = QTreeWidgetItem(self.treeWidgetLayers)
        new_tree_item.setText(0, layer_name)

        layer_class_instance = Layer(None, self.init_value)
        new_tree_item.setData(0, Qt.UserRole, layer_class_instance)

        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)

        label = QLabel(f"This is  {layer_name}")
        label.setWindowTitle(layer_name)  # Set the window title to the layer name
        label.setAlignment(Qt.AlignCenter)
        label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
        layout.addWidget(label)

        function_combo_box = QComboBox()
        function_combo_box.addItem("Select Function", None)
        function_combo_box.addItems(self.listForCombobox)
        layout.addWidget(function_combo_box)
        current_toplvlitem_index = self.treeWidgetLayers.indexOfTopLevelItem(new_tree_item)
        function_combo_box.currentIndexChanged.connect(lambda index: self.functionSelected(index, function_combo_box, page_widget, layer_class_instance, current_toplvlitem_index, layer_name))
        

        self.stackedWidget.addWidget(page_widget)

        new_tree_item.pageWidget = page_widget
        
    def removeLayer(self):
        # Remove selected layer and its corresponding page
        selectedItems = self.treeWidgetLayers.selectedItems()
        if selectedItems:
            item = selectedItems[0]
            index = self.treeWidgetLayers.indexOfTopLevelItem(item)
            self.treeWidgetLayers.takeTopLevelItem(index)
            self.stackedWidget.removeWidget(self.stackedWidget.widget(index))
        self.applyFunctionsAndShow()

    def changePage(self, current, _):
        # Change to the page corresponding to the selected tree item
        if current:
            self.stackedWidget.setCurrentWidget(current.pageWidget)

    def export(self):
        if self.base_image is not None:
            options = QFileDialog.Options()
            suggestedPath = os.path.join(os.getcwd(), self.currentFileName)  # Suggest the original file name in the current directory
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", suggestedPath,
                                                      "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
            if fileName:
                print(f"File selected for saving: {fileName}")
                cv.imwrite(fileName, img=self.final_image)
        else:
            print("No image loaded to save.")
        
#############################
                
    def functionSelected(self, index, combo_box, container_widget, layer_class_instance, current_toplvlitem_index, layer_name):
        if index > 0:
            selectedFunction = combo_box.currentText()
            layer_class_instance.update_function(getattr(Edit, combo_box.currentText()))
            #current_index = len(self.listOfFunctions) - 1
            #print(current_index)
            
            if selectedFunction == "brightness":
                
                label = QLabel("Brightness")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Brightness")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)


            elif selectedFunction == "contrast":

                label = QLabel("Contrast")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Contrast")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(2000)
                
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(1000)
                
                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Knee")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(0)
                slider_2.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(500)
            
                container_widget.layout().addItem(spacer)

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))
                combo_box.setVisible(False)
        
            elif selectedFunction == "saturation":
                
                label = QLabel("Saturation")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Saturation")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(2000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(1000)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)

            elif selectedFunction == "whitebalance":

                label = QLabel("WhiteBalance")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, WhiteBalance")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)

            elif selectedFunction == "offset":

                label_0 = QLabel("Offset")
                label_0.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                label = QLabel("Blue")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Offset")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                container_widget.layout().addWidget(label_0)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Green")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(-1000)
                slider_2.setMaximum(1000)
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(0)
                

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))

                label_3 = QLabel("Red")
                label_3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_3 = QSlider(Qt.Horizontal)
                slider_3.setMinimum(-1000)
                slider_3.setMaximum(1000)
                container_widget.layout().addWidget(label_3)
                container_widget.layout().addWidget(slider_3)
                slider_3.setValue(0)

                slider_3.valueChanged.connect(self.applyFunctionsAndShow)
                slider_3.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 2))


                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addItem(spacer)
                combo_box.setVisible(False)
                slider_2.setValue(1)
                slider_3.setValue(1)

            elif selectedFunction == "blur":

                label = QLabel("Blur")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Blur")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(5000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)

            elif selectedFunction == "sharpen":

                label = QLabel("Sharpen")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Sharpen")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(3000)
                
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                
                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Aplha")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(0)
                slider_2.setMaximum(3000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(1500)
            
                container_widget.layout().addItem(spacer)

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))
                combo_box.setVisible(False)

            elif selectedFunction == "filmgrain":

                label = QLabel("FilmGrain")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, FilmGrain")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(3000)
                
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                
                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Size")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(0)
                slider_2.setMaximum(3000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(1500)
            
                container_widget.layout().addItem(spacer)

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))
                combo_box.setVisible(False)

            elif selectedFunction == "log_shadows":

                label = QLabel("LogShadows")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, LogShadows")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(3000)
                
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(1000)
                
                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Baseline")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(0)
                slider_2.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(333)
            
                container_widget.layout().addItem(spacer)

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))
                combo_box.setVisible(False)

            elif selectedFunction == "lift":
                label = QLabel("Lift")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Lift")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)

            elif selectedFunction == "gain":
                label = QLabel("Gain")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Gain")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                combo_box.setVisible(False)

            elif selectedFunction == "lift_tint":
                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Lift Tint")
                label_0 = QLabel("Lift Tint")
                label_0.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
                label = QLabel("Blue")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(-1000)
                slider.setMaximum(1000)
                container_widget.layout().addWidget(label_0)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(0)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))

                label_2 = QLabel("Green")
                label_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_2 = QSlider(Qt.Horizontal)
                slider_2.setMinimum(-1000)
                slider_2.setMaximum(1000)
                container_widget.layout().addWidget(label_2)
                container_widget.layout().addWidget(slider_2)
                slider_2.setValue(0)

                slider_2.valueChanged.connect(self.applyFunctionsAndShow)
                slider_2.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 1))

                label_3 = QLabel("Red")
                label_3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

                slider_3 = QSlider(Qt.Horizontal)
                slider_3.setMinimum(-1000)
                slider_3.setMaximum(1000)
                container_widget.layout().addWidget(label_3)
                container_widget.layout().addWidget(slider_3)
                slider_3.setValue(0)

                slider_3.valueChanged.connect(self.applyFunctionsAndShow)
                slider_3.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 2))


                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addItem(spacer)
                combo_box.setVisible(False)

            elif selectedFunction == "negative":
                label = QLabel("Negative")
                label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))
                self.treeWidgetLayers.topLevelItem(current_toplvlitem_index).setText(0, f"{layer_name}, Negative")

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(1)
                slider.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
                spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                container_widget.layout().addWidget(label)
                container_widget.layout().addWidget(slider)
                slider.setValue(1)
                container_widget.layout().addItem(spacer)

                slider.valueChanged.connect(self.applyFunctionsAndShow)
                slider.valueChanged.connect(lambda value: self.sliderValueUpdater(value, layer_class_instance, 0))
                slider.setVisible(False)
                combo_box.setVisible(False)
                slider.setValue(0)

            else:
                pass 

##############################

    def sliderValueUpdater(self, value, layer_instance, arg_index):
        adjusted_value = value / 1000.0
        layer_instance.update_args(arg_index, adjusted_value)
        self.applyFunctionsAndShow()

#Classes
##################################################################

class Edit:

    def sigmoid(x, steepness=10):
        return 1 / (1 + np.exp(-x * steepness))
    
    @staticmethod
    def brightness(image, value):
        return np.clip(image + value, 0, 1)
    
    @staticmethod
    def contrast(image, factor, knee=0.5): 
        image_adjusted = knee + (image - knee) * factor
        image_adjusted = np.clip(image_adjusted, 0, 1)
        return image_adjusted
    
    @staticmethod
    def saturation(image, value): 
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV).astype(np.float32)
        hsv_image[:, :, 1] *= value
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 1)
        image_adjusted = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
        return image_adjusted
    
    @staticmethod
    def log_shadows(image, value, offset=0.333):
        sigmoid_mask = Edit.sigmoid((image - offset) * 10)
        shadows_adjustment = (offset - (offset - image) * value)
        image_no = ((1 - sigmoid_mask) * shadows_adjustment) + (sigmoid_mask * image)
        image_adjusted = np.clip(image_no, 0, 1)
        return image_adjusted
    
    @staticmethod
    def whitebalance(image, factor):
        image[:, :, 0] = image[:, :, 0] + factor * 1.4
        image[:, :, 1] = image[:, :, 1] + factor * 0.11
        image[:, :, 2] = image[:, :, 2] - factor * 0.9
        image_adjusted = np.clip(image, 0, 1)
        return image_adjusted
    
    @staticmethod
    def offset(image, blue=0, green=0, red=0):
        image[:, :, 0] += blue
        image[:, :, 1] += green
        image[:, :, 2] += red
        image_adjusted = np.clip(image, 0, 1)
        return image_adjusted
    
    @staticmethod  
    def blur(image, sigma):
        image_ycrcb = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)
        image_ycrcb[:, :, 0] = gaussian_filter(image_ycrcb[:, :, 0], sigma=sigma)
        image_adjusted = cv.cvtColor(image_ycrcb, cv.COLOR_YCrCb2BGR)
        return image_adjusted
        
    @staticmethod
    def sharpen(image, sigma=0, alpha=1.5):
        
        image_ycrcb = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)
        image_ycrcb_sharpen = image_ycrcb.copy()
        blurred_y = gaussian_filter(image_ycrcb[:, :, 0], sigma=sigma)
        
        unsharp_mask = image_ycrcb[:, :, 0] - blurred_y
        
        image_ycrcb_sharpen[:, :, 0] = image_ycrcb[:, :, 0] + alpha * unsharp_mask
        image_adjusted = cv.cvtColor(image_ycrcb_sharpen, cv.COLOR_YCrCb2BGR)
        image_adjusted = np.clip(image_adjusted, 0, 1)
        return image_adjusted

    @staticmethod
    def filmgrain(image, intensity=0.05, grain_size=1):
        grain = np.random.randn(*image.shape) * intensity 
        grain = gaussian_filter(grain, sigma=grain_size)
        image_with_grain = image + grain
        image_adjusted = np.clip(image_with_grain, 0, 1)
        return image_adjusted
    
    @staticmethod
    def lift(image, value):
        value = 1 - value
        lifted_image = 1 - (1 - image) * value
        image_adjusted = np.clip(lifted_image, 0, 1)
        return image_adjusted
    
    @staticmethod
    def gain(image, value):
        gain_iamge = image * (1 + value * (1 - image))
        image_adjusted = np.clip(gain_iamge, 0, 1)
        return image_adjusted

    @staticmethod
    def lift_tint(image, b=0, g=0, r=0):
        b = 1 - b
        g = 1 - g
        r = 1 - r
        image[:, :, 0] = 1 - (1 - image[:, :, 0]) * b
        image[:, :, 1] = 1 - (1 - image[:, :, 1]) * g 
        image[:, :, 2] = 1 - (1 - image[:, :, 2]) * r
        image_adjusted = np.clip(image, 0, 1)
        return image_adjusted
    
    @staticmethod
    def negative(image, _):
        image_negative = 1 - image
        image_adjusted = np.clip(image_negative, 0, 1)
        return image_adjusted
        

class Layer:
    def __init__(self, function=None, *args, **kwargs):
        self.function = function
        self.args = list(args)  # Store args as a list to facilitate updates
        self.kwargs = kwargs

    def update_args(self, index, value):
        if index < len(self.args):
            self.args[index] = value
        else:
            self.args += [None]*(index - len(self.args) + 1)
            self.args[index] = value

    def update_function(self, function_selected):
        self.function = function_selected


#RUN
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

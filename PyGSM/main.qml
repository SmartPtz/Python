import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2
import QtQuick.Extras 1.4
import QtQuick.Controls.Styles 1.4

ApplicationWindow {
    id: root
    visible: true
    Rectangle {
    width: 700
    height: 700
    color: "gray"

        Timer { id: network_timer;
        interval: 250; running: true; repeat: true
        onTriggered: test(); property int count: 0
        function test()   {

                           //console.log("test", count)
                           if (count == 0)
                           {network25.color="gray"; network50.color="gray"; network75.color="gray"; network100.color="gray"}
                           if (count == 25) {network25.color="darkcyan"}
                           if (count == 50) {network50.color="darkcyan"}
                           if (count == 75) {network75.color="darkcyan"}
                           if (count == 100) {network100.color="darkcyan"}
                           count = count + 25
                           if (count > 100) {count=0}
                            }
          }



        function network()                                 // javascript functions
          {
            if (value < 1000)
            {network_timer.start()}
            else {network25.color = "red"
                 network_timer.stop()
                 }
           }

        Item {
              x: 600; y: 50;

              Rectangle {
                        id: network25
                        x: 0; y: 30;
                        width: 15
                        height: 20
                        color: "gray"
                        border.color: "dimgray"
                        border.width: 3
                        radius: 4
                        //ColorAnimation on color { to: "yellow"; duration: 1000 }
                        }

              Rectangle {
                        id: network50
                        x: 12; y: 20;
                        width: 15
                        height: 30
                        color: "gray"
                        border.color: "dimgray"
                        border.width: 3
                        radius: 4
                        }
              Rectangle {
                        id: network75
                        x: 24; y: 10;
                        width: 15
                        height: 40
                        color: "gray"
                        border.color: "dimgray"
                        border.width: 3
                        radius: 4
                        }
              Rectangle {
                        id: network100
                        x: 36; y: 0;
                        width: 15
                        height: 50
                        color: "gray"
                        border.color: "dimgray"
                        border.width: 3
                        radius: 4

                        }

              }



        Text {
              text: new Date().toLocaleDateString(Qt.locale("en_EN"), "ddd MMMM d yyyy" )
        }


        StatusIndicator {
                        id: power_led
                        active : false
                        x: 100; y: 50;
                        width: 40
                        height: 40
                        color: "green"
                        }

                   Item {
                        x: 145; y: 45;
                        width: 40
                        height: 40
                                     Text {
                                           id: power_text
                                           visible: true
                                           font.pixelSize : 20
                                           font.bold: true
                                           text: "Off"
                                           anchors.horizontalCenter: parent.horizontalCenter
                                           anchors.bottom: parent.bottom
                                           color: "darkgrey"
                                           }
                        }

        StatusIndicator {
        id: status_led
        //anchors.centerIn: parent
        x: 100; y: 100;
        width: 40
        height: 40
        color: "green"
        }
        Item {
              x: 170; y: 90;
              width: 40
              height: 40
                  Text {
                       id: status_text
                       visible: true
                       font.pixelSize : 20
                       font.bold: true
                       text: "Off line"
                       anchors.horizontalCenter: parent.horizontalCenter
                       anchors.bottom: parent.bottom
                       color: "darkgrey"
                       }
             }

     }

     Connections {
        target: handler

        // Обработчик сигнала сложения
        onSumResult: {
            // sum было задано через arguments=['sum']
            //gauge.accelerating = true
            //gauge.value = sum
            //gauge.power_led = true
            console.log("handler", sum)
        }
     }

}
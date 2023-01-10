var myVideoStream = document.getElementById('myVideo')     // make it a global variable
var myStoredInterval = 0

function getVideo(){
    navigator.getMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    
    navigator.getMedia({video: true, audio: false},
                    
        function(stream) {
            myVideoStream.srcObject = stream   
            myVideoStream.play();
        }, 
                        
        function(error) {
        alert('webcam not working');
    });
}

function takeSnapshot() {
    var myCanvasElement = document.getElementById('myCanvas');
    var myCTX = myCanvasElement.getContext('2d');
    myCTX.drawImage(myVideoStream, 0, 0, myCanvasElement.width, myCanvasElement.height);
 
}

function saveImg() {

    var canvas = document.getElementById('myCanvas');
    const image = canvas.toDataURL("image/png", 1);

    const link = document.createElement("a");

    // link.src = "./images";
    link.href = image;
    link.download = "text_img";
    link.click();

  
}




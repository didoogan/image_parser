         var socket = null;
         var isopen = false;
         window.onload = function() {
            socket = new WebSocket("ws://127.0.0.1:9000");
            socket.binaryType = "arraybuffer";
            socket.onopen = function() {
               console.log("Connected!");
               isopen = true;
               sendText();
            };
            socket.onmessage = function(e) {
               if (typeof e.data == "string") {
                  console.log("Text message received: " + e.data);
                   var obj = JSON.parse(e.data);

                   // if(obj.hasOwnProperty('google')) {
                   //     var googleImg = JSON.parse(obj['google']);
                   //
                   //     googleImg.forEach(function (src) {
                   //         var img = document.createElement("img");
                   //         img.src = src;
                   //         var googleDiv = document.getElementById('google-img');
                   //         googleDiv.appendChild(img)
                   //     });
                   // }
                   renderEngineImgs(obj, 'google');
                   renderEngineImgs(obj, 'yandex');
                   renderEngineImgs(obj, 'instagram');



                   var img = document.createElement("img");
                   img.src = JSON.parse(e.data);
                   var p = document.createElement("p");
                   // p.innerHTML = JSON.parse(e.data);
                   // p.innerHTML = e.data;
                   console.log('data!!!!!!!!!!! ' + JSON.parse(e.data));

                   var src = document.getElementById("result");
                   src.appendChild(img);
                   
               } else {
                  var arr = new Uint8Array(e.data);
                  var hex = '';
                  for (var i = 0; i < arr.length; i++) {
                     hex += ('00' + arr[i].toString(16)).substr(-2);
                  }
                  console.log("Binary message received: " + hex);
               }
            }
            socket.onclose = function(e) {
               console.log("Connection closed.");
               socket = null;
               isopen = false;
            }
         };
         function sendText() {
            if (isopen) {
               // socket.send("Hello, Dima!");
               socket.send(query);
            } else {
               console.log("Connection not opened.")
            }
         };
         function sendBinary() {
            if (isopen) {
               var buf = new ArrayBuffer(32);
               var arr = new Uint8Array(buf);
               for (i = 0; i < arr.length; ++i) arr[i] = i;
               socket.send(buf);
               console.log("Binary message sent.");
            } else {
               console.log("Connection not opened.")
            }
         };
         function closeConnection() {
             socket.onclose();
         }


         function renderEngineImgs(obj,engine) {
             if (obj.hasOwnProperty(engine) && obj[engine][2] != null &&  obj[engine][2] != undefined) {
                 var h3 = document.createElement('h3');
                 h3.setAttribute("align", "center");
                 var text = engine[0].toUpperCase() + engine.slice(1) + " images :";
                 h3.appendChild(document.createTextNode(text));
                 var engineDiv = document.getElementById(engine+'-img');
                 engineDiv.appendChild(h3);

                 var images = JSON.parse(obj[engine]);

                 images.forEach(function (src) {
                     var img = document.createElement("img");
                     img.src = src;
                     img.className = "img-thumbnail";
                     engineDiv.appendChild(img)
                 });
             }
         }
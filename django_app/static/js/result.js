         var socket = null;
         var isopen = false;
         window.onload = function() {
            socket = new WebSocket("ws://127.0.0.1:9000");
            socket.binaryType = "arraybuffer";
            socket.onopen = function() {
               console.log("Connected!");
               isopen = true;
               sendText();
            }
            socket.onmessage = function(e) {
               if (typeof e.data == "string") {
                  console.log("Text message received: " + e.data);
                   var obj = JSON.parse(e.data)

                   if(obj.hasOwnProperty('google')) {
                       var googleImgs = obj['google']
                       googleImgs.forEach(function (src) {
                           var img = document.createElement("img");
                           img.src = src;
                           var googleDiv = document.getElementById('google-img');
                           googleDiv.appendChild(img)
                       })
                   }

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
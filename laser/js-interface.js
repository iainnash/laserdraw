const ffi = require("ffi");
const ref = require("ref");
const ArrayType = require("ref-array");
const Struct = require("ref-struct");
const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 8080 });

wss.on("connection", function connection(ws) {
  ws.on("message", message => {
    const data = JSON.parse(message).data;
    framesToDraw = [drawRawFrame(data)]; //drawFrame(data, 4)];
    let statusAttempts = 0;
    while (statusAttempts < 512 && libHeliosDac.GetStatus(0) !== 1) {
      console.log("status?");
    }
    console.log(framesToDraw[0].length);
    libHeliosDac.WriteFrame(
      0,
      20000,
      0b101,
      framesToDraw[0],
      framesToDraw[0].length
    );
  });
  ws.send("init");
});

const Frame = Struct({
  x: ref.types.uint16,
  y: ref.types.uint16,
  r: ref.types.uint8,
  g: ref.types.uint8,
  b: ref.types.uint8,
  i: ref.types.uint8
});
var FrameAry = ArrayType(Frame);

const libHeliosDac = ffi.Library("./libHeliosDacAPI", {
  OpenDevices: ["int", []],
  GetStatus: ["int", ["int"]],
  Stop: ["int", ["int"]],
  WriteFrame: ["bool", ["int", "int", "int", FrameAry, "int"]],
  CloseDevices: ["bool", []]
});

function drawRawFrame(data) {
  return data.map(pt => ({
    x: pt[0],
    y: pt[1],
    r: pt[2],
    g: pt[3],
    b: pt[4],
    i: 255,
  }));
}

function drawFrame(data, scale) {
  if (!scale) {
    scale = 1;
  }
  const res = [];
  data.forEach(set => {
    // x: set[0]//Math.floor(set[0][set[0].length-1] * scale),
    // y: set[1]//2000-Math.floor(set[1][set[1].length-1] * scale),
    // r: 0,
    // g: 0,
    // b: 0,
    set.map(item => {
      res.push({
        ...item,
        i: 255
      });
    });
    // for (let i = 0; i < set[0].length; i++) {
    //     for (let n = 0; n < 4; n++) {
    //         res.push({
    //             x: 800+Math.floor(set[0][i] * scale*1.3),
    //             y: 2000-Math.floor(set[1][i] * scale),
    //             r: 255,
    //             g: 255,
    //             b: 255,
    //             i: 255,
    //         });
    //     }
    // }
    // for (let i = 0 ; i < 3; i++) {
    //     res.push({
    //         x: Math.floor(set[0][set[0].length-1] * scale),
    //         y: 2000-Math.floor(set[1][set[1].length-1] * scale),
    //         r: 0,
    //         g: 0,
    //         b: 0,
    //         i: 0,
    //     });
    // }
  });
  const outNative = new FrameAry(res.length);
  for (let i = 0; i < res.length; i++) {
    outNative[i] = Frame(res[i]);
  }
  return outNative;
}

let framesToDraw = [
  drawFrame([
    [
      [
        102,
        102,
        107,
        115,
        122,
        154,
        162,
        165,
        169,
        229,
        255,
        217,
        187,
        168,
        166,
        165,
        160,
        90,
        89,
        27,
        0,
        35,
        97
      ],
      [
        0,
        8,
        17,
        22,
        23,
        19,
        14,
        5,
        6,
        47,
        74,
        110,
        99,
        95,
        97,
        156,
        202,
        190,
        91,
        107,
        54,
        41,
        8
      ]
    ]
  ]),
  drawFrame(
    [
      [
        [
          102,
          102,
          107,
          115,
          122,
          154,
          162,
          165,
          169,
          229,
          255,
          217,
          187,
          168,
          166,
          165,
          160,
          90,
          89,
          27,
          0,
          35,
          97
        ],
        [
          0,
          8,
          17,
          22,
          23,
          19,
          14,
          5,
          6,
          47,
          74,
          110,
          99,
          95,
          97,
          156,
          202,
          190,
          91,
          107,
          54,
          41,
          8
        ]
      ]
    ],
    1.5
  ),
  drawFrame(
    [
      [
        [
          102,
          102,
          107,
          115,
          122,
          154,
          162,
          165,
          169,
          229,
          255,
          217,
          187,
          168,
          166,
          165,
          160,
          90,
          89,
          27,
          0,
          35,
          97
        ],
        [
          0,
          8,
          17,
          22,
          23,
          19,
          14,
          5,
          6,
          47,
          74,
          110,
          99,
          95,
          97,
          156,
          202,
          190,
          91,
          107,
          54,
          41,
          8
        ]
      ]
    ],
    2
  )
];

libHeliosDac.OpenDevices();

while (libHeliosDac.GetStatus(0) === 0) {
  // wait for init
}
console.log("laser init");

// for (let i = 0; i < framesToDraw.length; i++) {
//     let statusAttempts = 0;
//     while (statusAttempts < 512 && libHeliosDac.GetStatus(0) !== 1) {

//     }
//     libHeliosDac.WriteFrame(0, 20000, 0, framesToDraw[i], framesToDraw[i].length);
//     console.log('frames at i', i);
// }

// setInterval(() => {
//     console.log('drawing', framesToDraw[0]);
//     const flags = 0b01110000;
//     libHeliosDac.WriteFrame(0, 20000, 0, framesToDraw[0], framesToDraw[0].length);
// }, 1000);

process.on("SIGINT", function() {
  libHeliosDac.Stop(0);
  // libHeliosDac.CloseDevices();
  process.exit();
});

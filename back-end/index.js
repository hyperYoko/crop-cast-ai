import express from "express";
import cors from "cors";
import { spawn } from "child_process";

const app = express();
app.use(cors());
app.use(express.json());

app.get('/predict', (req, res) => {
    const district = req.query.district;
    const crop = req.query.crop;
    const area = req.query.area;
    const soil = req.query.soil;
  
    const pythonProcess = spawn('python', ['predict.py', district, crop, area, soil]);
    var prediction = '';
    pythonProcess.stdout.on('data', (data) => {
      prediction = data.toString();
    });
  
    pythonProcess.stderr.on('data', (data) => {
      console.log(data.toString());
    });

    pythonProcess.on('close', (code) => {
      return res.send(prediction);
    });
  });

app.listen(8080, () => {console.log("Webserver at port 8080");});
  
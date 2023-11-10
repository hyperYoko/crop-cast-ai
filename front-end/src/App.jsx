import { useEffect, useState } from "react";
const inputLists = {
  districts: [
    "AHMEDNAGAR", "AKOLA", "AMRAVATI", "AURANGABAD", "BEED", "BHANDARA", "BULDHANA", "CHANDRAPUR", "DHULE", "GADCHIROLI",
    "GONDIA", "HINGOLI", "JALGAON", "JALNA", "KOLHAPUR", "LATUR", "NAGPUR", "NANDED", "NANDURBAR", "NASHIK",
    "OSMANABAD", "PARBHANI", "PUNE", "SANGLI", "SATARA", "SOLAPUR", "THANE", "WARDHA", "WASHIM", "YAVATMAL"
  ],
  crops: [
    "Jowar", "Bajra", "Wheat"
  ],
  soils: [
    "chalky", "clay", "loamy", "sandy", "silty"
  ]
};

function App() {
  const [district, setDistrict] = useState('');
  const [crop, setCrop] = useState('');
  const [area, setArea] = useState('');
  const [soil, setSoil] = useState('');
  const [prediction, setPrediction] = useState('');
  function showSpinner() {
    const button = document.querySelector('button');
    button.disabled = true;
    button.innerHTML = 'Predict... <span class="spinner">🧠</span>';
  }
  function hideSpinner() {
    const button = document.querySelector('button');
    button.disabled = false;
    button.innerHTML = 'Predict';
  }
  const handlePrediction = () => {
    showSpinner();
    const url = `http://localhost:8080/predict?district=${district}&crop=${crop}&area=${area}&soil=${soil}`;
    fetch(url)
      .then((response) => response.text())
      .then((data) => {
        setPrediction(data);
        document.getElementById('prediction').style.display = 'block';
        hideSpinner();
      })
      .catch((error) => {
        console.error('Prediction error:', error);
      });
      
  };

  return (
    <div class="container p-5 page">
        <div class="card col-6 p-0 mx-auto">
            <div class="card-header text-primary text-center">
                <h3>Crop Cast AI</h3>
                <h5>Crop Yield Prediction using ML</h5>
            </div>
            <div class="card-body">
                <div class="form-group">
                    <label for="district">District:</label>
                    <select class="form-control" name="district" id="district" onChange={(e) => setDistrict(e.target.value)}>
                      <option hidden disabled selected value> Select district </option>  
                      {inputLists.districts.map((option) => (<option key={option} value={option}>{option}</option>))}
                    </select>
                </div>
                <div class="form-group">
                    <label for="crop">Crop:</label>
                    <select class="form-control" name="crop" id="crop" onChange={(e) => setCrop(e.target.value)}>
                      <option hidden disabled selected value> Select crop </option>
                      {inputLists.crops.map((option) => (<option key={option} value={option}>{option}</option>))}
                    </select>
                </div>
                <div class="form-group">
                    <label for="area">Area(in acres):</label>
                    <input type="number" min="100" max="10000000" class="form-control" id="area" placeholder="Enter area" onChange={(e) => setArea(e.target.value)}/>
                </div>
                <div class="form-group">
                    <label for="soil">Soil:</label>
                    <select class="form-control" name="soil" id="soil" onChange={(e) => setSoil(e.target.value)}>
                      <option hidden disabled selected value> Select soil </option> 
                      {inputLists.soils.map((option) => (<option key={option} value={option}>{option}</option>))}
                    </select>
                </div>
                <div class="row">
                    <button class="btn btn-primary mx-auto" id="submit" onClick={handlePrediction}>Predict</button>
                </div>
            </div>
            <div class="card-footer" id="prediction" style={{ display: 'none' }}>
              {prediction}
            </div>
        </div>
    </div>
  );
}

export default App

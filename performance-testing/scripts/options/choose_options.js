import load from "./load.js";
import sample from "./sample.js";
import stress from "./stress.js";
const TEST_TYPE = __ENV.TEST_TYPE || 'stress';

export default function chooseOptions(scenario){
    switch (TEST_TYPE) {
        case "stress":
            console.log("Running Stress Test")
            return stress(scenario)
        case "load":
            console.log("Running Load Test")
            return load(scenario)
        default:
            console.log("Running Sample Test")
            return sample(scenario)
    }
}

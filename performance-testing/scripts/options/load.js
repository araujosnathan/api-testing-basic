import { data } from "../utils/data.js"

const ENV = __ENV.ENV || 'local';
const date = new Date().toISOString()

export default function load(scenario) {
  return  {
    ext: {
      loadimpact: {
        projectID: data.k6_project_cloud_id,
        name: `${ENV.toUpperCase()} - LOAD - ${scenario} - ${date} `
      }
    },
    scenarios: {
      stress: {
        executor: "ramping-arrival-rate",
        preAllocatedVUs: 100,
        timeUnit: "1s",
        stages: [
          { duration: '5s', target: 2 }, 
          { duration: '5s', target: 2 },
          { duration: '15s', target: 8 }, 
          { duration: '15s', target: 8 },
          { duration: '5s', target: 2 }, 
          { duration: '5s', target: 2 },
          { duration: '2s', target: 0 },
        ]
      },
    },
  }
};

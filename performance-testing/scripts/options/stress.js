import { data } from "../utils/data.js";

const ENV = __ENV.ENV || 'local';
const date = new Date().toISOString()

export default function stress(scenario) {
  return {
    ext: {
      loadimpact: {
        projectID: data["k6_project_cloud_id"],
        name: `${ENV.toUpperCase()} - STRESS - ${scenario} - ${date} `
      }
    },
    scenarios: {
      stress: {
        executor: "ramping-arrival-rate",
        preAllocatedVUs: 100,
        timeUnit: "1s",
        stages: [
          { duration: "2s", target: 4 },
          { duration: "2s", target: 4 },
          { duration: "5s", target: 6 },
          { duration: "5s", target: 6 },
          { duration: "10s", target: 8 },
          { duration: "10s", target: 8 },
          { duration: "15s", target: 10 },
          { duration: "15s", target: 10 },
          { duration: "10s", target: 8 },
          { duration: "10s", target: 8 },
          { duration: "5s", target: 6 },
          { duration: "5s", target: 6 },
          { duration: "30s", target: 0 },
        ],
      },
    },
    // This is only a example. If you already know your data-driver, implement here your thresholds. If you know the limit
    // of your application, comment this part. 
    thresholds: {
      http_req_duration: ["p(95)<200", "p(99)<300"], 
      http_req_failed: ["rate<0.1"],
    },
  }
};

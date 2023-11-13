import { data } from "../utils/data.js"

const ENV = __ENV.ENV || 'local';
const date = new Date().toISOString()

export default function sample(scenario) {
  return {
    ext: {
      loadimpact: {
        projectID: data.k6_project_cloud_id,
        name: `${ENV.toUpperCase()} - SAMPLE - ${scenario} - ${date} `
      }
    },
    stages: [
      { duration: "2", target: 5 },
    ],
  }
};

import http from 'k6/http';
import { check, fail } from 'k6';
import { data } from './utils/data.js';
import chooseOptions from './options/choose_options.js';
import createTestUser from './utils/create_user.js'
const title = "POST /booking";

export let options = chooseOptions(title);

const ENV = __ENV.ENV || 'local';
const url = `${data[ENV].api_service_base_url}/booking`;

export function setup() {
  const userCreated = createTestUser(ENV)
  console.log(userCreated)
  const bookingPayload = JSON.stringify({
    "date": "2023-11-06",
    "destination": "GRU",
    "origin": "MAD",
    "userId": userCreated.id
  });
  console.log(bookingPayload);
  return { bookingBody: bookingPayload };
}

export default function createBooking(data) {
  const headers = {
    "Content-Type": "application/json",
  };
  const response = http.post(url, data.bookingBody, {headers});
  console.log(response.body);
  
  if (!check(response, {
    "Create Booking Success": res => res.status === 201
  })) {
    fail(`Unexpected Status Code: ${response.status}`);
  }
}

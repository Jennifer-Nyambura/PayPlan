const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5555/";

//  Generic request helper

export async function request(path, { method = "GET", body, token, isForm = false } = {}) {
  const headers = {};

  if (token && !isForm) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (!isForm) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  });

  let data;
  try {
    data = await res.json();
  } catch (e) {
    data = null;
  }

  if (!res.ok) {
    throw { status: res.status, message: data?.message || "Request failed", data };
  }

  return data;
}

//  LOGIN request 
 
export async function loginRequest(email, password) {
  return request("/login", {
    method: "POST",
    body: { email, password },
  });
}

//  SIGNUP request
 
export async function signupRequest(payload) {
  return request("/signup", {
    method: "POST",
    body: payload,
  });
}


//  Fetch current user 
 
export async function fetchCurrentUser(token) {
  return request("/me", {
    method: "GET",
    token,
  });
}

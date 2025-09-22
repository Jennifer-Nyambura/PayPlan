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
  } catch {
    data = null;
  }

  if (!res.ok) {
    throw { status: res.status, message: data?.message || "Request failed", data };
  }

  return data;
}

// LOGIN request
export async function loginRequest(email, password) {
  // Backend returns { access_token: "..." }
  return request("/login", {
    method: "POST",
    body: { email, password },
  });
}

// SIGNUP request 
export async function signupRequest(payload) {
  return request("/signup", {
    method: "POST",
    body: payload,
  });
}

// Fetch current user (protected route)
export async function fetchCurrentUser(token) {
  return request("/me", {
    method: "GET",
    token,
  });
}

/* DASHBOARD HELPERS */

// Fetch all services
export async function getServices(token) {
  return request("/services", {
    method: "GET",
    token,
  });
}

// Fetch upcoming payments
export async function getUpcomingPayments(token) {
  return request("/payments/upcoming", {
    method: "GET",
    token,
  });
}

// Fetch overdue payments
export async function getOverduePayments(token) {
  return request("/payments/overdue", {
    method: "GET",
    token,
  });
}

// Mark payment as paid
export async function markPaymentAsPaid(paymentId, token) {
  return request(`/payments/${paymentId}/pay`, {
    method: "POST",
    token,
  });
}

export class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async handleErrors(response) {
    const contentType = response.headers.get("Content-Type") || "";
    // const clonedResponse = response.clone();

    if (response.ok) {
      if (contentType.includes("application/json")) {
        return await response.json(); // Parse JSON response
      }
    }

    if (response.status === 204) {
      return {};
    }

    if (response.status >= 400) {
      if (response.status === 401) {
        return {
          error:
            "Unauthorized. Please refresh the page. If this persists, login again.",
        };
      }

      if (response.status === 429) {
        if (contentType.includes("application/json")) {
          const errorResponse = await response.json();
          const errorMessage = errorResponse.errors;

          try {
            const match = errorMessage.match(/(\d+) second(s)?/);
            return {
              error: `Validation already sent. Please try again in ${match[1]} seconds.`,
            };
          } catch (error) {
            console.error("Error parsing error message:", error);
            return { error: `Validation already sent. Please try again.` };
          }
        }
      }

      if (contentType.includes("application/json")) {
        try {
          const errorData = await response.json();
          if (errorData.errors) {
            return { error: errorData.errors }; // Return specific error
          }
        } catch (e) {
          console.error("Error parsing error response:", e);
          return { error: "Unexpected error occurred." };
        }
      } else {
        return { error: "Unexpected error occurred." };
      }

      // try { // only for debugging
      //   // Non-JSON error response
      //   const errorText = await clonedResponse.text();

      //   // Handle the error message here
      //   return { error: errorText || 'Unexpected error occurred. Something went wrong' };
      // } catch (err) {
      //   console.error('Error while reading the error response body:', err);
      //   return { error: 'Unexpected error occurred. Something went wrong' };
      // };
    }

    if (response.status >= 500) {
      return { error: "Server error" }; // Server-side error
    }

    throw new Error("Unexpected error occurred.");
  }

  async request(
    endpoint,
    method,
    data = null,
    additionalOptions = {},
    isMultipart = false,
  ) {
    const url = `${this.baseURL}${endpoint}`;

    let options = {
      method,
      headers: {
        Accept: "application/json",
      },
      credentials: "include",
      ...additionalOptions,
    };

    if (isMultipart && data instanceof FormData) {
      // For multipart/form-data
      delete options.headers["Content-Type"];
      options.body = data;
    } else if (data) {
      // For application/json
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);
      return await this.handleErrors(response);
    } catch (error) {
      console.error("Fetch error:", error);
      throw error;
    }
  }

  async get(endpoint, additionalOptions = {}) {
    return await this.request(endpoint, "GET", null, additionalOptions);
  }

  async post(endpoint, data, additionalOptions = {}, isMultipart = false) {
    return await this.request(
      endpoint,
      "POST",
      data,
      additionalOptions,
      isMultipart,
    );
  }

  async patch(endpoint, data, additionalOptions = {}, isMultipart = false) {
    return await this.request(
      endpoint,
      "PATCH",
      data,
      additionalOptions,
      isMultipart,
    );
  }

  async put(endpoint, data, additionalOptions = {}, isMultipart = false) {
    return await this.request(
      endpoint,
      "PUT",
      data,
      additionalOptions,
      isMultipart,
    );
  }

  async delete(endpoint, data = null, additionalOptions = {}) {
    return await this.request(endpoint, "DELETE", data, additionalOptions);
  }

  stream(endpoint, onMessageCallback, onErrorCallback, onOpenCallback) {
    const url = `${this.baseURL}${endpoint}`;
    console.log(`Opening SSE connection to: ${url}`);
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      console.log("Raw SSE event received:", event.data);
      try {
        const data = JSON.parse(event.data);
        console.log("Parsed SSE message:", data);
        onMessageCallback(data);
      } catch (e) {
        console.error("Error parsing SSE message:", e);
        if (onErrorCallback) onErrorCallback(e);
      }
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error for URL:", url, error);
      if (onErrorCallback) onErrorCallback(error);
    };

    eventSource.onopen = () => {
      console.log("EventSource connection opened for URL:", url);
      if (onOpenCallback) onOpenCallback();
    };

    return eventSource;
  }
}

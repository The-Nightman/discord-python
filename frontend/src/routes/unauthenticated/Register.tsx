import axios from "axios";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { Toast } from "../../components/UX/Toast";
import { Spinner } from "../../components/UX/Spinner";
import { Link, useNavigate } from "react-router-dom";

interface FormData {
  email: string;
  username: string;
  password: string;
}

/**
 * The `Register` component provides a user interface for registering an account
 * with the application. It includes form fields for entering a username, email
 * and password, and handles form submission to authenticate the user.
 *
 * @component
 * @returns {JSX.Element} The rendered register form component.
 *
 * @example
 * ```tsx
 * import { Register } from './Register';
 *
 * const App = () => (
 *   <div>
 *     <Register />
 *   </div>
 * );
 * ```
 */
export const Register = (): JSX.Element => {
  const [valid, setValid] = useState<boolean>(true);
  const [error, setError] = useState<{ state: boolean; message: string }>({
    state: false,
    message: "",
  });
  // This object structure is required due to OAuth2PasswordRequestForm dependency in FastAPI
  const [formData, setFormData] = useState<FormData>({
    email: "",
    username: "",
    password: "",
  });
  const [loading, setLoading] = useState<boolean>(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  /**
   * Handles the change event for input elements and updates the form data state.
   *
   * @param {React.ChangeEvent<HTMLInputElement>} event - The change event triggered by the input element.
   * @returns {void}
   */
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  /**
   * Validates the email field on blur event.
   *
   * - If the email field is empty, sets the valid state to true and returns early.
   * - Uses a regex pattern to validate the email as an email address.
   *
   * The regex pattern used is sourced from the regexr community by Chris Bane at https://regexr.com/3ashn.
   * It is tested on regexr to work better than the RFC2822 email regex and follows validation rules and samples from:
   * http://en.wikipedia.org/wiki/Email_address#Invalid_email_addresses
   *
   * @returns {void}
   */
  const validateOnBlur = (): void => {
    // If the email field is empty, set the valid state to false and return early
    // The input is marked as required, so this alongside backend checks should not cause issues
    if (formData.email === "") {
      setValid(true);
      return;
    }

    // This rediculous regex is from regexr community by Chris Bane at https://regexr.com/3ashn
    // Desc: Validation rules and samples taken from here: http://en.wikipedia.org/wiki/Email_address#Invalid_email_addresses
    // It actually works better than the RFC2822 email regex
    const validRegex =
      /^(?:(?:[\w`~!#$%^&*\-=+;:{}'|,?\/]+(?:(?:\.(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)*"|[\w`~!#$%^&*\-=+;:{}'|,?\/]+))*\.[\w`~!#$%^&*\-=+;:{}'|,?\/]+)?)|(?:"(?:\\?[\w`~!#$%^&*\-=+;:{}'|,?\/\.()<>\[\] @]|\\"|\\\\)+"))@(?:[a-zA-Z\d\-]+(?:\.[a-zA-Z\d\-]+)*|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])$/.test(
        formData.email
      );

    setValid(validRegex);
  };

  /**
   * Handles the form submission for the sign up form.
   *
   * @remarks - Unlike the login form, the register form requires the addition of a
   * username and sends data as json in the body.
   *
   * Prevents the default form submission behavior, constructs the request parameters,
   * and sends a POST request to the register API endpoint. On successful registration,
   * it calls the `login` function with the access token. If an error occurs, it sets
   * the error state with an appropriate message.
   *
   * @param {React.FormEvent<HTMLFormElement>} event - The form submission event.
   * @returns {Promise<void>} A promise that resolves when the form submission is complete.
   */
  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    event.preventDefault(); // Prevent the page from refreshing on submit
    setError({ state: false, message: "" }); // Reset the error state incase of previous errors with a still open toast
    setLoading(true); // Set loading state to true

    try {
      // Send a POST request to the register endpoint and extract data object on success
      const { data }: { data: { access_token: string; token_type: string } } =
        await axios.post(
          "http://localhost:8000/api/v1/accounts/register",
          formData
        );
      login(data.access_token);
      setLoading(false); // Set loading state to false
      navigate("/app"); // Navigate to the dashboard on success
    } catch (error) {
      setLoading(false); // Set loading state to false
      // This gives us access to AxiosError properties interfaces
      if (axios.isAxiosError(error)) {
        // Check if error.response is defined
        if (error.response) {
          setError({ state: true, message: error.response.data.detail });
        } else {
          // Edge case: typically error.response is undefined in cases such as a network error
          // If the error response is undefined, set a generic error message unless one is supplied
          setError({
            state: true,
            message: error.message ?? "An unknown error occurred.", // Nullish coalescing is honestly more readable than ternaries
          });
        }
      }
    }
  };

  return (
    <main className="min-w-72">
      <Toast
        show={error.state}
        message={error.message}
        windowMode={true}
        colour="error"
        animate={true}
        onClose={() => setError({ state: false, message: "" })}
        autoCloseDuration={8000}
      />
      <div className="flex flex-col items-center">
        <h1 className="text-white text-2xl font-semibold">Welcome!</h1>
        <p className="text-gray-300">You're almost there!</p>
      </div>
      <form
        name="register form"
        className="flex flex-col mt-8 gap-8"
        onSubmit={(e) => handleSubmit(e)}
      >
        <fieldset className="flex flex-col gap-6">
          <legend className="sr-only">Sign Up</legend>
          <div className="relative z-0 w-full group">
            <input
              type="username"
              name="username"
              id="username"
              className="block py-2.5 px-0 w-full text-base text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-300 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
              placeholder=""
              required
              aria-required="true"
              aria-labelledby="UsernameLabel"
              aria-description="Please choose a username for your account."
              value={formData.username}
              onChange={(e) => handleChange(e)}
            />
            <label
              id="UsernameLabel"
              htmlFor="username"
              className="peer-focus:font-medium absolute text-base text-gray-300 font-semibold duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
            >
              Username
            </label>
          </div>
          <div className="relative z-0 w-full group">
            <input
              type="email"
              name="email"
              id="email"
              className={`block py-2.5 px-0 w-full text-base text-gray-900 bg-transparent border-0 border-b-2 ${
                valid
                  ? "border-gray-300 dark:border-gray-300"
                  : "border-red-500 dark:border-red-500"
              } appearance-none dark:text-white dark:border-gray-300 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer`}
              placeholder=""
              required
              aria-required="true"
              aria-labelledby="EmailLabel"
              aria-description="Please enter your the email address for your account."
              aria-invalid={valid}
              value={formData.email}
              onChange={(e) => handleChange(e)}
              onBlur={() => validateOnBlur()}
            />
            <label
              id="EmailLabel"
              htmlFor="email"
              className="peer-focus:font-medium absolute text-base text-gray-300 font-semibold duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
            >
              Email
            </label>
          </div>
          <div className="relative z-0 w-full group">
            <input
              type="password"
              name="password"
              id="password"
              className={`block py-2.5 px-0 w-full text-base text-gray-900 bg-transparent border-0 border-b-2 appearance-none dark:text-white dark:border-gray-300 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer`}
              placeholder=""
              minLength={8}
              required
              aria-required="true"
              aria-labelledby="PasswordLabel"
              aria-description="Please choose password at least 8 characters long."
              value={formData.password}
              onChange={(e) => handleChange(e)}
            />
            <label
              id="PasswordLabel"
              htmlFor="password"
              className="peer-focus:font-medium absolute text-base text-gray-300 font-semibold duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6"
            >
              Password
            </label>
            <strong className="text-white text-xs font-normal">
              Min 8 characters
            </strong>
          </div>
        </fieldset>
        <button
          className="w-full py-2.5 text-base font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600 active:bg-blue-400 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50 shadow-md"
          aria-label="Sign Up"
          name="signup"
          type="submit"
        >
          Sign Up
        </button>
      </form>
      <div className="flex gap-1 mt-4">
        <p className="text-white text-xs">Already have an account?</p>
        <Link className="text-xs text-[#5CD6FE] hover:underline" to={"/"}>
          Login
        </Link>
      </div>
      {loading && <Spinner />}
    </main>
  );
};

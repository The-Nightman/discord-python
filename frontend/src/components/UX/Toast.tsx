import { useEffect, useRef, useState } from "react";
import { AiOutlineCloseCircle } from "react-icons/ai";

interface ToastPropsBase {
  show: boolean;
  message: string;
  textSize?: string;
  windowMode?: boolean;
  colour?: "success" | "error" | "warning" | "info";
  onClose?: () => void;
  animate?: boolean;
}

interface AutoCloseProps {
  onClose: () => void;
  autoCloseDuration: number;
}

type ToastProps = ToastPropsBase &
  (
    | AutoCloseProps
    | { autoCloseDuration?: undefined; autoCloseFunction?: undefined }
  );

/**
 * Toast component to display a notification message.
 *
 * @param {ToastProps} props - The props of the component.
 * @param {boolean} props.show - Determines whether the toast is visible.
 * @param {string} props.message - The message to display inside the toast.
 * @param {boolean} props.windowMode - If true, positions the toast at the top of the screen, else follows 
 * document flow however relative style is present allowing it to be used inside an element with position
 * absolute in order to present from underneath that element.
 * @param {string} props.colour - The colour type of the toast (success, error, warning, info).
 * @param {() => void} props.onClose - Callback function to close the toast.
 * @param {number} props.autoCloseDuration - Duration in milliseconds after which the toast will automatically close,
 * ensure that the chosen time gives less able users or screen readers plenty of time to read the component.
 * @param {boolean} props.animate - If true, applies animation to the toast entrance.
 *
 * @returns {JSX.Element} The rendered Toast component.
 */
export const Toast = ({
  show,
  message,
  windowMode,
  colour,
  onClose,
  autoCloseDuration,
  animate,
}: ToastProps): JSX.Element => {
  const toastRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    // get the height of the toast element and set it to the state for use in translation transition
    if (toastRef.current) {
      setHeight(toastRef.current.offsetHeight);
    }

    // if show is true and autoCloseDuration is set, close the toast after the set duration
    if (show && autoCloseDuration) {
      const timer = setTimeout(() => {
        onClose();
      }, autoCloseDuration);
      return () => clearTimeout(timer);
    }
  }, [show]);

  // Define the colour types and their corresponding tailwind
  const colourTypes: Record<string, string> = {
    success: "bg-green-500",
    error: "bg-red-500",
    warning: "bg-amber-500",
    info: "bg-blue-500",
  };

  // Set the dynamic style object properties as arbitrary
  // tailwind classes wont work with template literal interpolation
  const styleObject: Record<string, string> = {
    // Static for default, absolute for window mode to position at top of the screen
    ...(windowMode && {
      position: "absolute",
      top: `-${height}px`,
      left: "0px",
    }),
    transform: `translateY(${height}px)`,
  };

  return (
    <>
      {show && (
        <div
          ref={toastRef}
          className={`relative w-full py-4 px-6 flex
            ${animate ? "animate-in" : ""} 
            ${colourTypes[colour ?? "success"]}  
            ${onClose ? "justify-between" : "justify-center"}
            items-center gap-4 rounded shadow-md duration-500 z-50`}
          style={{ ...styleObject }}
          role="alert"
          aria-live={colour === "error" || "warning" ? "assertive" : "polite"}
        >
          <p className="text-white font-semibold">{message}</p>
          {onClose && (
            <button
              onClick={onClose}
              className="text-white"
              name="close"
              aria-label="Close"
            >
              <AiOutlineCloseCircle />
            </button>
          )}
        </div>
      )}
    </>
  );
};

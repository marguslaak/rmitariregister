import { type ToastOptions, toast } from 'react-toastify';

const initialOptions: ToastOptions = {
  bodyClassName: 'toast-container',
  position: 'top-right',
  autoClose: 5000,
  hideProgressBar: true,
  closeOnClick: false,
  pauseOnHover: false,
  draggable: false,
};

export const sendSuccessToast = ({
  content,
  toastOptions,
}: {
  content: string;
  toastOptions?: ToastOptions;
}) =>
  toast.success(<div className="success-toast">{content}</div>, {
    ...initialOptions,
    ...toastOptions,
  });

export const sendErrorToast = ({
  content,
  toastOptions,
}: {
  content: string;
  toastOptions?: ToastOptions;
}) =>
  toast.error(<div className="error-toast">{content}</div>, {
    ...initialOptions,
    ...toastOptions,
  });

export const NAVBAR_HEIGHT = "70px";

type ErrorBoxProps = {
    error: string;
    warning?: string;
    info?: string;
    success?: string;
};

const ErrorBox = ({ error, warning, info, success }: ErrorBoxProps) => {

    return (
        <div className="w-100 container">
            {error && (
                <div className="w-100 text-danger border border-2 border-danger p-2 bg-darker rounded-3">
                    {error}
                </div>
            )}
            {warning && (
                <div className="w-100 text-warning border border-2 border-warning p-2 bg-darker rounded-3">
                    {warning}
                </div>
            )}
            {info && (
                <div className="w-100 text-info border border-2 border-info p-2 bg-darker rounded-3">
                    {info}
                </div>
            )}
            {success && (
                <div className="w-100 text-success border border-2 border-success p-2 bg-darker rounded-3">
                    {success}
                </div>
            )}
        </div>
    );
};

export default ErrorBox;

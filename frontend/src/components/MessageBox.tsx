type MessageBoxProps = {
    error?: string;
    warning?: string;
    info?: string;
    success?: string;
};

const MessageBox = ({ error, warning, info, success }: MessageBoxProps) => {

    const boxStyle = (color: string) => `w-100 text-${color} border text-center border-2 border-${color} p-3 bg-${color}-subtle-dark rounded-3`;

    return (
        <div className="w-100 d-flex flex-column gap-2">
            {error && (
                <div className={boxStyle("danger")}>
                    {error}
                </div>
            )}
            {warning && (
                <div className={boxStyle("warning")}>
                    {warning}
                </div>
            )}
            {info && (
                <div className={boxStyle("info")}>
                    {info}
                </div>
            )}
            {success && (
                <div className={boxStyle("success")}>
                    {success}
                </div>
            )}
        </div>
    );
};

export default MessageBox;

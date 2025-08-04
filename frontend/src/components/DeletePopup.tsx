import { useEffect, useState } from "react";

import ShortTextField from "@/components/fields/ShortTextField";

import MessageBox from "@/components/MessageBox";
import Modal from "@/components/design/Modal";
import ButtonField from "@/components/fields/ButtonField";

type DeletePopupProps = {
    showModal: boolean;
    setShowModal: (show: boolean) => void;
    title?: string;
    children?: React.ReactNode;
    onConfirm?: (input?: any) => void | Promise<void>;
    onCancel?: (input?: any) => void | Promise<void>;

    typeConfirmText?: string;
};

export default function DeletePopup({ showModal, setShowModal, title, children, onConfirm, onCancel, typeConfirmText }: DeletePopupProps) {
    const [confirmInput, setConfirmInput] = useState<string>("");

    const [tabNumber, setTabNumber] = useState<number>(0);

    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");

    const handleConfirm = async () => {
        if (onConfirm) {
            try {
                setLoading(true);
                if(typeConfirmText && confirmInput !== typeConfirmText) {
                    setError("Confirmation text does not match.");
                    setLoading(false);
                    return;
                }

                await onConfirm();
                setShowModal(false);
            } catch (err: any) {
                setError(err.message || "An error occurred while confirming. Please try again.");
            } finally {
                setLoading(false);
            }
        }
    };

    const handleCancel = () => {
        if (onCancel) {
            onCancel();
        }
        setConfirmInput("");
        setShowModal(false);
    };

    return (
        <Modal
            title={title || "Confirm Action"}
            showModal={showModal}
            setShowModal={setShowModal}
            onClose={handleCancel}
            height="auto"
            width="50"
            >
            <div className="d-flex flex-column gap-3 overflow-y-auto text-center">

                {children && (
                    <div className="text-light">
                        {children}
                        <p className="text-warning"><strong>WARNING:</strong> THIS ACTION IS IRREVERSIBLE</p>
                    </div>
                )}

                {typeConfirmText && (
                    <>
                        <p className="text-muted">
                            Type "<strong className="text-danger">{typeConfirmText}</strong>" to confirm this action.
                            <br/>
                            <small className="text-muted">(Case Sensitive)</small>
                            <br/>
                        </p>

                        <ShortTextField
                            value={confirmInput}
                            setValue={(value) => setConfirmInput(value)}
                            placeholder={`Type "${typeConfirmText}"`}
                            disabled={loading}
                        />
                    </>
                )}

                {error && <MessageBox error={error} />}

                <hr />

                <div className="d-flex flex-row gap-3">
                    <ButtonField 
                        onClick={handleCancel}
                        loading={loading}
                        color="dark"
                        rounding="3"
                    >
                        Cancel
                    </ButtonField>
                    <ButtonField 
                        onClick={handleConfirm}
                        loading={loading}
                        color="danger"
                        rounding="3"
                    >
                        Confirm
                    </ButtonField>
                </div>
            </div>
        </Modal>
    );
}
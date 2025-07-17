import AccountLayout from "@layouts/AccountLayout";
import ProfileForm from "@features/account/ProfileForm";

export default function AccountProfilePage() {

    return (
        <AccountLayout>
            <div className="w-100 h-100 rounded-5 p-4 bg-dark text-start">
                <h1 className="text-light">Profile Settings</h1>
                <ProfileForm />
            </div>
        </AccountLayout>
    );
}

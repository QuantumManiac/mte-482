import clsx from "clsx";

interface ActionButtonProps {
    icon?: string;
    text: string;
    style?: string;
    onClick?: () => void;
    disabled?: boolean;
}

export default function ActionButton({ icon, text, onClick, disabled, style }: ActionButtonProps) {
    return (
        <button disabled={disabled} onClick={onClick} className={`w-20 flex flex-col justify-center items-center ${style}`}>
            {icon && <span className="text-2xl">{icon}</span>}
            <span className={clsx({
                "text-2xl": !icon
            })}>{text}</span>
        </button>
    );
}

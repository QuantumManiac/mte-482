interface ActionButtonProps {
    icon?: string;
    text: string;
    style?: string;
    onClick?: () => void;
    disabled?: boolean;
}

export default function ActionButton({ icon, text, onClick, disabled, style }: ActionButtonProps) {
    return (
        <button disabled={disabled} onClick={onClick} className={`w-24 flex flex-col justify-center items-center ${style}`}>
            {icon && <span className="text-3xl">{icon}</span>}
            <span>{text}</span>
        </button>
    );
}

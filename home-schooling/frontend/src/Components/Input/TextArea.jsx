const TextArea = ({
  placeholder,
  name,
  handleChange,
  value,
  type,
  disabled,
  handleFocus,
  handleBlur,
  classes,
  label,
  icon,
}) => {
  return (
    <div className="my-1 h-full">
      {label && (
        <label className="font-semibold text-sm text-white ">{label}</label>
      )}

      <textarea
        className={`outline-none w-full h-full bg-white justify-between items-center mt-2 border  px-5 py-3 rounded-lg ${
          classes ? classes : "h-32"
        }`}
        placeholder={placeholder}
        type={type}
        name={name}
        value={value}
        disabled={disabled}
        onChange={handleChange}
      />
    </div>
  );
};

export default TextArea;

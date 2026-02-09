/**
 * AddKnowledgeButton - Button to open the add knowledge modal
 */

import React from 'react';

interface AddKnowledgeButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

export const AddKnowledgeButton: React.FC<AddKnowledgeButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  return (
    <button
      className="add-knowledge-button"
      onClick={onClick}
      disabled={disabled}
      title={disabled ? 'Login required to add knowledge' : 'Add new definition'}
    >
      + Add Definition
    </button>
  );
};

export default AddKnowledgeButton;

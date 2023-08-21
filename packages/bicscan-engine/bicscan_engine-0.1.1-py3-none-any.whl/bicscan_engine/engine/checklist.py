ERC20_CHECKLIST = {
    "18160ddd": "totalSupply",
    "70a08231": "balanceOf",
    "a9059cbb": "transfer",
    "23b872dd": "transferFrom",
    "095ea7b3": "approve",
    "dd62ed3e": "allowance",
    "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "event Transfer",
    "8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925": "event Approval",
}

ERC721_CHECKLIST = {
    "70a08231": "balanceOf",
    "6352211e": "ownerOf",
    "b88d4fde": "safeTransferFrom",
    "42842e0e": "safeTransferFrom",
    "23b872dd": "transferFrom",
    "095ea7b3": "approve",
    "a22cb465": "setApprovalForAll",
    "081812fc": "getApproved",
    "e985e9c5": "isApprovedForAll",
    "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef": "event Transfer",
    "8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925": "event Approval",
    "17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31": "event ApprovalForAll",
}

ERC1155_CHECKLIST = {
    "f242432a": "safeTransferFrom",
    "2eb2c2d6": "safeBatchTransferFrom",
    "00fdd58e": "balanceOf",
    "4e1273f4": "balanceOfBatch",
    "a22cb465": "setApprovalForAll",
    "e985e9c5": "isApprovedForAll",
    "c3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62": "event TransferSingle",
    "4a39dc06d4c0dbc64b70af90fd698a233a518aa5d07e595d983b8c0526c8f7fb": "event TransferBatch",
    "17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31": "event ApprovalForAll",
    "6bb7ff708619ba0610cba295a58592e0451dee2622938c8755667688daf3529b": "event URI",
}

SIMPLE_ERC20_CHECKLIST = {
    "06fdde03": "name",
    "95d89b41": "symbol",
    "18160ddd": "totalSupply",
}

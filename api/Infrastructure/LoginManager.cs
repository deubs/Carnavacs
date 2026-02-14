using Carnavacs.Api.Domain;
using Carnavacs.Api.Domain.Entities;
using Carnavacs.Api.Infrastructure.Interfaces;
using System.Security.Cryptography;
using System.Text;

namespace Carnavacs.Api.Infrastructure
{
    public class LoginManager
    {
        private readonly IConfiguration _config;
        private readonly IUnitOfWork _unitOfWork;
        private readonly TokenHandler _tokenHandler;

        public LoginManager(IConfiguration config, IUnitOfWork unitOfWork, TokenHandler tokenHandler)
        {
            _config = config;
            _unitOfWork = unitOfWork;
            _tokenHandler = tokenHandler;
        }

        public async Task<LoginResponse> Login(LoginModel login)
        {
            var user = await _unitOfWork.Users.GetByUsernameAsync(login.Username);
            if (user == null)
                throw new Exception("Invalid credentials");

            var validationKey = _config["Membership:ValidationKey"];
            using var hmac = new HMACSHA1 { Key = HexToByte(validationKey) };
            var encoded = Convert.ToBase64String(hmac.ComputeHash(Encoding.Unicode.GetBytes(login.Password)));

            if (encoded != user.Password)
                throw new Exception("Invalid credentials");

            var roles = await _unitOfWork.Users.GetRolesByUserIdAsync(user.Id);
            user.Roles = roles;

            var token = _tokenHandler.BuildToken(user);

            return new LoginResponse
            {
                Token = token,
                User = user
            };
        }

        private static byte[] HexToByte(string hexString)
        {
            var bytes = new byte[hexString.Length / 2];
            for (int i = 0; i < bytes.Length; i++)
            {
                bytes[i] = Convert.ToByte(hexString.Substring(i * 2, 2), 16);
            }
            return bytes;
        }
    }

    public class LoginResponse
    {
        public string Token { get; set; }
        public User User { get; set; }
    }
}
